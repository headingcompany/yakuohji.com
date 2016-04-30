<?php

#inc ���������
include_once 'inc/inc_base.inc';

#Zend
require_once 'Zend/Filter/StripTags.php';			//�ե��륿[HTML��PHP����]����ݡ��ͥ��

#func
include_once 'db/func_dbRead.inc';		//DB�ե��󥯥�����ɤ߹���
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

	//SEO
		if ($con == "") { $con = "����"; }
		if (!$db11ary = dbRead('db11_cntlist','db11_cntname',$con)) {
			$db11ary = dbRead('db11_cntlist','db11_cntname','����');
		};
	//�⡼��
		if ($mode == "" or $mode == "") {
			$step[0] = "on";
			$cnts = 'tpl_req00Rule.tpl';
		}
		elseif ($mode == "inp") {
			$step[1] = "on";
			$cnts = 'tpl_req01Inp.tpl';
		}
		elseif ($mode == "inppsnl") {
			$step[2] = "on";
		}
		elseif ($mode == "enq") {
			$step[3] = "on";
		}
		elseif ($mode == "chk") {
			$step[4] = "on";
		}
		elseif ($mode == "end") {
			$step[5] = "on";
		}


?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=euc-jp" />
<title><?=$db11ary[0]['db11_cnth1']?> < <?=$db11ary[0]['db11_cnttit']?> | ���������� | ������˭���� ��������߻Ԥˤ���ĤĤ��Τ���</title>
<meta name="description" content="<?=$db11ary[0]['db11_cntdesc']?>��������߻Ԥˤ��롢������˭���ɤΤ����������������Ǥ���">
<meta name="keywords" content="<?=$db11ary[0]['db11_cntkwds']?>,������,˭��,��,����,����,��Ҷ���,���Ķ���,�ĤĤ�,����">
<link href="common/css/common.css" rel="stylesheet" type="text/css" />
<link href="common/css/req.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div class="w800px mT10px autoM">
	<h1 class="flL"><a href="/" target="_self" class="title ti bDisp"><?=$db11ary[0]['db11_cnth1']?> < <?=$db11ary[0]['db11_cnttit']?> | ���������� | ������˭���� ��������߻Ԥˤ���ĤĤ��Τ���</a></h1>
	<div class="w545px flR relPosi clearfix">
		<div class="contents txt w510px p5px mT25px">
			<h2>������Τ���������</h2>
			<br />
			<ul class="w480px step nonMp autoM clearfix">
				<li class="flL <?=$step[0]?>">�Ϥ����</li>
				<li class="flL <?=$step[1]?>">������������</li>
				<li class="flL <?=$step[2]?>">���������</li>
				<li class="flL <?=$step[3]?>">���󥱡���</li>
				<li class="flL <?=$step[4]?>">���Ƥγ�ǧ</li>
				<li class="flL <?=$step[5]?>">��λ</li>
			</ul>
			<br />
			<? include $cnts; ?>
		</div>
		<ul class="menu1 nonMark nonMp abPosi">
			<li class="flL"><a href="/main.html" target="_self" class="menu1_info bDisp ti">���Τ餻</a></li>
			<li class="flL"><a href="/greet.html" target="_self" class="menu2_greet bDisp ti">����������</a></li>
			<li class="flL"><a href="/his.html" target="_self" class="menu3_history bDisp ti">���</a></li>
		</ul>
		<ul class="menu2 nonMark abPosi">
			<li><a href="/garden.html" target="_self" class="menu4_garden bDisp ti">����</a></li>
			<li><a href="/schedule.html" target="_self" class="menu5_event bDisp ti">�Ի�����</a></li>
			<li><a href="/info.html" target="_self" class="menu6_contact bDisp ti">����礻</a></li>
			<li><a href="/link.html" target="_self" class="menu7_link bDisp ti">���</a></li>
			<li><a href="/special.html" target="_self" class="menu8_special bDisp ti">���ߥڡ���</a></li>
		</ul>
	</div>
	<hr size="1" color="#ffffff" class="foot">
	<span class="foot flR">copyright(C) <a href="/" target="_self">yakuohji</a>.</span>
</div>
<!--Google Anaylytics����������-->
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-779505-9");
pageTracker._trackPageview();
} catch(err) {}</script>
<!--Google Anaylytics�������ޤ�-->
</body>
</html>