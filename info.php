<?php

#inc 初期値設定
include_once 'inc/inc_base.inc';

#Zend
require_once 'Zend/Filter/StripTags.php';			//フィルタ[HTML・PHP除去]コンポーネント
require_once 'Zend/Validate/EmailAddress.php';		//メールアドレス正規判定コンポーネント
require_once 'Zend/Validate/Alnum.php';				//文字が英数字のみで構成されているか判定するコンポーネント
require_once 'Zend/Mail.php';						//メール送信コンポーネント
require_once 'Zend/Mail/Transport/Sendmail.php';	//メール送信コンポーネント

#func
include_once 'sub/func_setCookies.inc';	//サブファンクション：クッキー格納
include_once 'sub/func_getCookies.inc';	//サブファンクション：クッキー取得
include_once 'sub/func_optNumMake.inc';	//サブファンクション：2桁数値オプション生成
include_once 'sub/func_inpMake.inc';	//サブファンクション：インプット+ラベル自動生成

	//引数受け取り
		if ($_POST != "") {
			foreach ($_POST as $postname => $postarg) {
				$$postname = new Zend_Filter_StripTags();	//HTML・PHP除去
				if (!mb_check_encoding($postarg,'EUC-JP')) {
					$postarg = mb_convert_encoding($postarg, "EUC-JP");
				}
				$$postname = $postarg;
			}
		}
		if ($_GET != "") {
			foreach ($_GET as $postname => $postarg) {
				$$postname = new Zend_Filter_StripTags();	//HTML・PHP除去
				if (!mb_check_encoding($postarg,'EUC-JP')) {
					$postarg = mb_convert_encoding($postarg, "EUC-JP");
				}
				$$postname = $postarg;
			}
		}

	//入力情報チェック
		if ($mode == "chk") {

			//inc DBフィールド名設定 db01_memebr
			include 'inc/inc_array_value_yakuohji_info.inc';

			//必須項目展開
				foreach ($array_sql_value_must as $postname_must => $postarg_must) {
					if ($$postarg_must == "") {
						$err[$postarg_must] = $postarg_must;
					}
				}

			//マルチバイト確認
				//ふりがなのみチェック
				foreach ($array_txtmltbyte as $postname => $postarg) {
					//ひらがな確認
					if (!mb_ereg("^[ぁ-ん\ \　]{1,10}$",$$postarg)) {
						//unMatchの場合、$err[変数名]に値を代入
						$err[$postarg] = $$postarg;
					}
				}

			//ID（メールアドレス）チェック
				//メールアドレスの正規性チェック
				foreach ($array_txtmail as $postname => $postarg) {
					//メールアドレスと判定されない場合false
					$valEmail = new Zend_Validate_EmailAddress();
					if (!$valEmail->isValid($$postarg)) {
						//unMatchの場合、$err[変数名]に値を代入
						$err[$postarg] = $$postarg;
					}
				}

			//エラー状況による分岐
				if ($err == "") {
					$i=0;
					//foreach ($array_sql_value as $postname => $postarg) {
					foreach ($array_sql_value_must as $postname => $postarg) {
						//array配列を単純配列に変換
						if ($i == 0) {
							$cookie_array_postarg = $$postarg;
							$i++;
						} else {
							$cookie_array_postarg .= ",".$$postarg;
						}
					}
					//クッキーへの格納
					$value = setCookies($cookieName,$cookie_array_postarg);

				} else {
					//エラー・入力情報の修正
						$mode = "err";
					//エラー表示のためのフィールド名代入
						foreach ($err as $postname => $postarg) {
							$errDisp[$postname] = 'bDisp';
						}
						$smarty->assign('errDisp', $errDisp);
					//Smarty 変数代入
						foreach ($array_sql_value_must as $postname => $postarg) {
							$smarty->assign($postarg,$$postarg);
						}
				}

		}



	//入力・再入力・エラー時の修正
		if ($mode == "" or $mode == "inp" or $mode == "re" or $mode == "err") {

			//inc DBフィールド名設定 db01_memebr
				include 'inc/inc_array_value_yakuohji_info.inc';

			//修正時
				if ($mode == "re") {
					//クッキー取得
						if ($cookie_array = getCookies($cookieName,',')) {
							//データの配列作成
								$i=0;
								foreach ($array_sql_value_must as $postname => $postarg) {
									$$postarg = $cookie_array[$i];
									$i++;
								}
							//Smarty 変数代入
								foreach ($array_sql_value_must as $postname => $postarg) {
									$smarty->assign($postarg,$$postarg);
								}
						}
				}

			//質問の選択肢を生成
				if ($ques == "") { $ques = "お通夜・ご葬儀について"; }			//性別が空欄の場合、男性とする
				$inp_ques = inpMake('ques','radio',$inpMake_value_array_yakuohji_info_ques,$inpMake_id_array_yakuohji_info_ques,$inpMake_txt_array_yakuohji_info_ques,$ques);
				$smarty->assign('inp_ques', $inp_ques);
		}

	//入力情報の確認
		if ($err == "" && $mode == "chk") {
			//Smarty配列作成
			foreach ($array_sql_value_must as $postname => $postarg) {
				$smarty->assign($postarg,$$postarg);
			}
		}

	//DB書込み
		if ($mode == "end") {
			//inc DBフィールド名設定 db01_memebr
				include 'inc/inc_array_value_yakuohji_info.inc';

			//登録データの配列作成
			//クッキーからの復元
			//クッキー取得
				if ($cookie_array = getCookies($cookieName,',')) {
					//クッキーの内容を配列へ格納
						$i=0;
						foreach ($array_sql_value_must as $postname => $postarg) {
							$$postarg = $cookie_array[$i];
							$i++;
						}

					//質問→薬王寺メール

						$rs_Sub = '[薬王寺]お問合せがありました';
						$rs_Body= '薬王寺Webサイトからお問合せがありました。

お名前： '.$name.'（'.$kana.'）
メールアドレス： '.$mail.'
質問内容： '.$ques.'
本文：
'.$text.'


';
						$sendmail = new Zend_Mail('ISO-2022-JP');
						$sendmail->setFrom($mail);
						$sendmail->addTo('info@yakuohji.com');
						$sendmail->addBcc('takashi@hdg.jp');
						$sendmail->setSubject(mb_convert_encoding($rs_Sub, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->setBodyText(mb_convert_encoding($rs_Body, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->send();


					//薬王寺→質問者メール
						$rs_Sub = '[薬王寺]お問合せありがとうございます';
						$rs_Body= $name.'様

この度は薬王寺へお問い合わせいただきありがとうございました。

ご記入いただいたメールアドレスに送信内容をメールいたしましたので、ご確認ください。
なおご質問には迅速に対応いたしますが、諸事情により連絡が遅くなる場合もございますので、
ご了承ください。

以下にお寄せいただいたお問合せの内容を記載します。
ご確認いただければ幸いです。

質問内容： '.$ques.'
本文：
'.$text.'


--------------------------------------------------------------------------
真言宗豊山派 七国山薬王寺

info@yakuohji.com

';

						$sendmail = new Zend_Mail('ISO-2022-JP');
						$sendmail->setFrom('info@yakuohji.com');
						$sendmail->addTo($mail);
						$sendmail->addBcc('takashi@hdg.jp');
						$sendmail->setSubject(mb_convert_encoding($rs_Sub, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->setBodyText(mb_convert_encoding($rs_Body, 'ISO-2022-JP', 'EUC-JP'));
						$sendmail->send();

					//クッキーの削除
						setcookie ($cookieName,'',0);
				} else {
					$mode = "inp";
				}

		}

//表示
	if ($mode == "" or $mode == "inp" or $mode == "re" or $mode == "err") { $smarty->display('_yakuohji_info_inp.tpl'); }	//入力・再入力・エラー時の修正
	elseif ($mode == "chk") { $smarty->display('_yakuohji_info_chk.tpl'); }													//入力情報の確認
	elseif ($mode == "end") { $smarty->display('_yakuohji_info_end.tpl'); }													//完了
	else { $smarty->display('_yakuohji_info_inp.tpl'); }																	//異常系入力


?>