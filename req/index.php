<?php

#inc 初期値設定
include_once 'inc/inc_base.inc';

#Zend
require_once 'Zend/Filter/StripTags.php';			//フィルタ[HTML・PHP除去]コンポーネント

#func
include_once 'db/func_dbRead.inc';		//DBファンクション：読み込み
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

	//SEO
		if ($con == "") { $con = "祈願"; }
		if (!$db11ary = dbRead('db11_cntlist','db11_cntname',$con)) {
			$db11ary = dbRead('db11_cntlist','db11_cntname','祈願');
		};
	//モード
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
<title><?=$db11ary[0]['db11_cnth1']?> < <?=$db11ary[0]['db11_cnttit']?> | 七国山薬王寺 | 真言宗豊山派 東京都青梅市にあるつつじのお寺</title>
<meta name="description" content="<?=$db11ary[0]['db11_cntdesc']?>東京都青梅市にある、真言宗豊山派のお寺・七国山薬王寺です。">
<meta name="keywords" content="<?=$db11ary[0]['db11_cntkwds']?>,真言宗,豊山,派,祈願,護摩,水子供養,先祖供養,つつじ,開花">
<link href="common/css/common.css" rel="stylesheet" type="text/css" />
<link href="common/css/req.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div class="w800px mT10px autoM">
	<h1 class="flL"><a href="/" target="_self" class="title ti bDisp"><?=$db11ary[0]['db11_cnth1']?> < <?=$db11ary[0]['db11_cnttit']?> | 七国山薬王寺 | 真言宗豊山派 東京都青梅市にあるつつじのお寺</a></h1>
	<div class="w545px flR relPosi clearfix">
		<div class="contents txt w510px p5px mT25px">
			<h2>ご祈願のお申し込み</h2>
			<br />
			<ul class="w480px step nonMp autoM clearfix">
				<li class="flL <?=$step[0]?>">はじめに</li>
				<li class="flL <?=$step[1]?>">お申込み内容</li>
				<li class="flL <?=$step[2]?>">送付先情報</li>
				<li class="flL <?=$step[3]?>">アンケート</li>
				<li class="flL <?=$step[4]?>">内容の確認</li>
				<li class="flL <?=$step[5]?>">完了</li>
			</ul>
			<br />
			<? include $cnts; ?>
		</div>
		<ul class="menu1 nonMark nonMp abPosi">
			<li class="flL"><a href="/main.html" target="_self" class="menu1_info bDisp ti">お知らせ</a></li>
			<li class="flL"><a href="/greet.html" target="_self" class="menu2_greet bDisp ti">ごあいさつ</a></li>
			<li class="flL"><a href="/his.html" target="_self" class="menu3_history bDisp ti">歴史</a></li>
		</ul>
		<ul class="menu2 nonMark abPosi">
			<li><a href="/garden.html" target="_self" class="menu4_garden bDisp ti">境内</a></li>
			<li><a href="/schedule.html" target="_self" class="menu5_event bDisp ti">行事日程</a></li>
			<li><a href="/info.html" target="_self" class="menu6_contact bDisp ti">お問合せ</a></li>
			<li><a href="/link.html" target="_self" class="menu7_link bDisp ti">リンク</a></li>
			<li><a href="/special.html" target="_self" class="menu8_special bDisp ti">特設ページ</a></li>
		</ul>
	</div>
	<hr size="1" color="#ffffff" class="foot">
	<span class="foot flR">copyright(C) <a href="/" target="_self">yakuohji</a>.</span>
</div>
<!--Google Anaylytics：ここから-->
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-779505-9");
pageTracker._trackPageview();
} catch(err) {}</script>
<!--Google Anaylytics：ここまで-->
</body>
</html>