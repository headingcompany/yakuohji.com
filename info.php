<?php

#inc ���������
include_once 'inc/inc_base.inc';

#Zend
require_once 'Zend/Filter/StripTags.php';			//�ե��륿[HTML��PHP����]����ݡ��ͥ��
require_once 'Zend/Validate/EmailAddress.php';		//�᡼�륢�ɥ쥹����Ƚ�ꥳ��ݡ��ͥ��
require_once 'Zend/Validate/Alnum.php';				//ʸ�����ѿ����Τߤǹ�������Ƥ��뤫Ƚ�ꤹ�륳��ݡ��ͥ��
require_once 'Zend/Mail.php';						//�᡼����������ݡ��ͥ��
require_once 'Zend/Mail/Transport/Sendmail.php';	//�᡼����������ݡ��ͥ��

#func
include_once 'sub/func_setCookies.inc';	//���֥ե��󥯥���󡧥��å�����Ǽ
include_once 'sub/func_getCookies.inc';	//���֥ե��󥯥���󡧥��å�������
include_once 'sub/func_optNumMake.inc';	//���֥ե��󥯥����2����ͥ��ץ��������
include_once 'sub/func_inpMake.inc';	//���֥ե��󥯥���󡧥���ץå�+��٥뼫ư����

	//�����������
		if ($_POST != "") {
			foreach ($_POST as $postname => $postarg) {
				$$postname = new Zend_Filter_StripTags();	//HTML��PHP����
				if (!mb_check_encoding($postarg,'EUC-JP')) {
					$postarg = mb_convert_encoding($postarg, "EUC-JP");
				}
				$$postname = $postarg;
			}
		}
		if ($_GET != "") {
			foreach ($_GET as $postname => $postarg) {
				$$postname = new Zend_Filter_StripTags();	//HTML��PHP����
				if (!mb_check_encoding($postarg,'EUC-JP')) {
					$postarg = mb_convert_encoding($postarg, "EUC-JP");
				}
				$$postname = $postarg;
			}
		}

	//���Ͼ�������å�
		if ($mode == "chk") {

			//inc DB�ե������̾���� db01_memebr
			include 'inc/inc_array_value_yakuohji_info.inc';

			//ɬ�ܹ���Ÿ��
				foreach ($array_sql_value_must as $postname_must => $postarg_must) {
					if ($$postarg_must == "") {
						$err[$postarg_must] = $postarg_must;
					}
				}

			//�ޥ���Х��ȳ�ǧ
				//�դ꤬�ʤΤߥ����å�
				foreach ($array_txtmltbyte as $postname => $postarg) {
					//�Ҥ餬�ʳ�ǧ
					if (!mb_ereg("^[��-��\ \��]{1,10}$",$$postarg)) {
						//unMatch�ξ�硢$err[�ѿ�̾]���ͤ�����
						$err[$postarg] = $$postarg;
					}
				}

			//ID�ʥ᡼�륢�ɥ쥹�˥����å�
				//�᡼�륢�ɥ쥹�������������å�
				foreach ($array_txtmail as $postname => $postarg) {
					//�᡼�륢�ɥ쥹��Ƚ�ꤵ��ʤ����false
					$valEmail = new Zend_Validate_EmailAddress();
					if (!$valEmail->isValid($$postarg)) {
						//unMatch�ξ�硢$err[�ѿ�̾]���ͤ�����
						$err[$postarg] = $$postarg;
					}
				}

			//���顼�����ˤ��ʬ��
				if ($err == "") {
					$i=0;
					//foreach ($array_sql_value as $postname => $postarg) {
					foreach ($array_sql_value_must as $postname => $postarg) {
						//array�����ñ��������Ѵ�
						if ($i == 0) {
							$cookie_array_postarg = $$postarg;
							$i++;
						} else {
							$cookie_array_postarg .= ",".$$postarg;
						}
					}
					//���å����ؤγ�Ǽ
					$value = setCookies($cookieName,$cookie_array_postarg);

				} else {
					//���顼�����Ͼ���ν���
						$mode = "err";
					//���顼ɽ���Τ���Υե������̾����
						foreach ($err as $postname => $postarg) {
							$errDisp[$postname] = 'bDisp';
						}
						$smarty->assign('errDisp', $errDisp);
					//Smarty �ѿ�����
						foreach ($array_sql_value_must as $postname => $postarg) {
							$smarty->assign($postarg,$$postarg);
						}
				}

		}



	//���ϡ������ϡ����顼���ν���
		if ($mode == "" or $mode == "inp" or $mode == "re" or $mode == "err") {

			//inc DB�ե������̾���� db01_memebr
				include 'inc/inc_array_value_yakuohji_info.inc';

			//������
				if ($mode == "re") {
					//���å�������
						if ($cookie_array = getCookies($cookieName,',')) {
							//�ǡ������������
								$i=0;
								foreach ($array_sql_value_must as $postname => $postarg) {
									$$postarg = $cookie_array[$i];
									$i++;
								}
							//Smarty �ѿ�����
								foreach ($array_sql_value_must as $postname => $postarg) {
									$smarty->assign($postarg,$$postarg);
								}
						}
				}

			//���������������
				if ($ques == "") { $ques = "�����롦���򵷤ˤĤ���"; }			//���̤�����ξ�硢�����Ȥ���
				$inp_ques = inpMake('ques','radio',$inpMake_value_array_yakuohji_info_ques,$inpMake_id_array_yakuohji_info_ques,$inpMake_txt_array_yakuohji_info_ques,$ques);
				$smarty->assign('inp_ques', $inp_ques);
		}

	//���Ͼ���γ�ǧ
		if ($err == "" && $mode == "chk") {
			//Smarty�������
			foreach ($array_sql_value_must as $postname => $postarg) {
				$smarty->assign($postarg,$$postarg);
			}
		}

	//DB�����
		if ($mode == "end") {
			//inc DB�ե������̾���� db01_memebr
				include 'inc/inc_array_value_yakuohji_info.inc';

			//��Ͽ�ǡ������������
			//���å������������
			//���å�������
				if ($cookie_array = getCookies($cookieName,',')) {
					//���å��������Ƥ�����س�Ǽ
						$i=0;
						foreach ($array_sql_value_must as $postname => $postarg) {
							$$postarg = $cookie_array[$i];
							$i++;
						}

					//���䢪�������᡼��

						$rs_Sub = '[������]����礻������ޤ���';
						$rs_Body= '������Web�����Ȥ��餪��礻������ޤ�����

��̾���� '.$name.'��'.$kana.'��
�᡼�륢�ɥ쥹�� '.$mail.'
�������ơ� '.$ques.'
��ʸ��
'.$text.'


';
						$sendmail = new Zend_Mail('ISO-2022-JP');
						$sendmail->setFrom($mail);
						$sendmail->addTo('info@yakuohji.com');
						$sendmail->addBcc('takashi@hdg.jp');
						$sendmail->setSubject(mb_convert_encoding($rs_Sub, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->setBodyText(mb_convert_encoding($rs_Body, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->send();


					//������������ԥ᡼��
						$rs_Sub = '[������]����礻���꤬�Ȥ��������ޤ�';
						$rs_Body= $name.'��

�����٤��������ؤ��䤤��碌�����������꤬�Ȥ��������ޤ�����

�����������������᡼�륢�ɥ쥹���������Ƥ�᡼�뤤�����ޤ����Τǡ�����ǧ����������
�ʤ�������ˤϿ�®���б��������ޤ�����������ˤ��Ϣ���٤��ʤ���⤴�����ޤ��Τǡ�
��λ������������

�ʲ��ˤ��󤻤�������������礻�����Ƥ򵭺ܤ��ޤ���
����ǧ����������й����Ǥ���

�������ơ� '.$ques.'
��ʸ��
'.$text.'


--------------------------------------------------------------------------
������˭���� ����������

info@yakuohji.com

';

						$sendmail = new Zend_Mail('ISO-2022-JP');
						$sendmail->setFrom('info@yakuohji.com');
						$sendmail->addTo($mail);
						$sendmail->addBcc('takashi@hdg.jp');
						$sendmail->setSubject(mb_convert_encoding($rs_Sub, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->setBodyText(mb_convert_encoding($rs_Body, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->send();

					//���å����κ��
						setcookie ($cookieName,'',0);
				} else {
					$mode = "inp";
				}

		}

//ɽ��
	if ($mode == "" or $mode == "inp" or $mode == "re" or $mode == "err") { $smarty->display('_yakuohji_info_inp.tpl'); }	//���ϡ������ϡ����顼���ν���
	elseif ($mode == "chk") { $smarty->display('_yakuohji_info_chk.tpl'); }													//���Ͼ���γ�ǧ
	elseif ($mode == "end") { $smarty->display('_yakuohji_info_end.tpl'); }													//��λ
	else { $smarty->display('_yakuohji_info_inp.tpl'); }																	//�۾������


?>