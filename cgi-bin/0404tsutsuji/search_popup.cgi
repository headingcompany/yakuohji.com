#!/usr/bin/perl
#
# 簡易データベース v2.1 (SJIS)　検索用
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

#データベースファイル
$file = "./tsutsuji.txt";

#１ページの表示数
$page = 1;

#-----------------------------------------------------------------------------------

#■入力

if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

if ($buffer eq "") { &error('エラー','使い方が間違っています.'); }

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name,$value) = split(/=/, $pair);
	$name2 = $name;
	$value2 = $value;
	$FORM2{$name} = $value;

	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value,'euc');

	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/\n//g;
	$value =~ s/\r//g;
	$value =~ s/\t//g;
	$value =~ s/\,//g;

	#フォーム変数へ
	$FORM{$name} = $value;
}

#■検索処理

if (!open(IN,"$file")) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

if ($FORM{'FF'} eq '') { $FF = 0; } else { $FF = $FORM{'FF'}; }
$TO = $FF + $page - 1;
if ($TO > $#BASE) { $TO = $#BASE; }
$hit = 0;
$next_num = '';

foreach $num ($FF .. $#BASE) {

	$data = $data2 = $BASE[$num];
	&jcode'convert(*data,'euc');
	($ID,$DATE,$COM,%GW,%GH,$NOTE) = split(/\,/,$data);

	# 日付ID(一致)

	if ($FORM{'ID'} ne 'all') {

		if ($ID eq $FORM{'ID'}) { ; } else { next; }
	}


	# 検索終了処理
	if ($hit == $page) { $next_num = $num; last; }
	else { push(@NEW,$data2); $hit++; }
}

#■検索結果

	($ID,$DATE,$COM,%GW,%GH,$NOTE) = split(/\,/,$data);

print "Content-type: text/html\n\n";
print <<"EOF";

<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=utf-8">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE>薬王寺のツツジ</TITLE>
<SCRIPT language="JavaScript">
<!--HPB_SCRIPT_ROV_50
//
//Licensed Materials - Property of IBM
//11P5743
//(C) Copyright IBM Corp. 1998, 2000 All Rights Reserved.
//

// HpbImgPreload:
//
function HpbImgPreload()
{
var appVer=parseInt(navigator.appVersion);
var isNC=(document.layers && (appVer >= 4));
var isIE=(document.all&& (appVer >= 4));
if (isNC || isIE)
{
if (document.images)
{
var imgName = HpbImgPreload.arguments[0];
var cnt;
swImg[imgName] = new Array;
for (cnt = 1; cnt < HpbImgPreload.arguments.length; cnt++)
{
swImg[imgName][HpbImgPreload.arguments[cnt]] = new Image();
swImg[imgName][HpbImgPreload.arguments[cnt]].src = HpbImgPreload.arguments[cnt];
}
}
}
}
// HpbImgFind:
//
function HpbImgFind(doc, imgName)
{
for (var i=0; i < doc.layers.length; i++)
{
var img = doc.layers[i].document.images[imgName];
if (!img) img = HpbImgFind(doc.layers[i], imgName);
if (img) return img;
}
return null;
}
// HpbImgSwap:
//
function HpbImgSwap(imgName, imgSrc)
{
var appVer=parseInt(navigator.appVersion);
var isNC=(document.layers && (appVer >= 4));
var isIE=(document.all&& (appVer >= 4));
if (isNC || isIE)
{
if (document.images)
{
var img = document.images[imgName];
if (!img) img = HpbImgFind(document, imgName);
if (img) img.src = imgSrc;
}
}
}
var swImg; swImg=new Array;
//-->
</SCRIPT><SCRIPT language="JavaScript">
<!--HPB_SCRIPT_PLD_50
HpbImgPreload('_HPB_ROLLOVER1', 'http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_09.gif', 'http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_over_09.gif');
//-->
</SCRIPT>
<STYLE type="text/css">
<!--
TD{
font-size : 16px;
}
-->
</STYLE>
</HEAD>
<BODY leftmargin="0" rightmargin="0" topmargin="0" marginwidth="0" marginheight="0" bgcolor="#ffffff">


EOF


if (!@NEW) {
print <<"EOF";
<center>●ご指定の条件では見当たりませんでした.
</center>
<!--Google Anaylytics：ここから-->
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-779505-5";
urchinTracker();
</script>
<!--Google Anaylytics：ここまで-->
</BODY>
</HTML>
EOF
exit;
}
else {



	foreach $data (@NEW) {

print <<"EOF";
<center>
<TABLE border="0" cellpadding="0" cellspacing="0">
<TBODY>
<TR>
<TD>
<TABLE border="0" width="100%" cellpadding="0" cellspacing="0">
<TBODY>
<TR>
<TD width="10"><IMG src="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_01.gif" width="10" height="29" alt=""></TD>

EOF
	($ID,$DATE,$COM,%GW,%GH,$NOTE) = split(/\,/,$data);


print <<"EOF";


<TD background="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_02.gif"><B>薬王寺のツツジ：$DATE</B></TD>
<TD width="3"><IMG src="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_03.gif" width="3" height="29" alt=""></TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
<TR>
<TD>
<TABLE border="0" cellpadding="0" cellspacing="0" width="100%">
<TBODY>
<TR>
<TD background="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_04.gif" width="3"></TD>
<TD>
<IMG src="http://www.t-net.ne.jp/~yakuohji/images/tsutsuji_w$ID.jpg">
</TD>
<TD width="3" background="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_06.gif"></TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
<TR>
<TD>
<TABLE border="0" cellpadding="0" cellspacing="0" width="100%">
<TBODY>
<TR>
<TD width="10"><IMG src="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_07.gif" width="10" height="23" alt=""></TD>
<TD background="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_08.gif"><font style="font-size:1px">.</font></TD>
<TD width="77"><A href="Javascript:window.close()" id="_HPB_ROLLOVER1" onmouseout="HpbImgSwap('_HPB_ROLLOVER1', 'http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_09.gif');" onmouseover="HpbImgSwap('_HPB_ROLLOVER1', 'http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_over_09.gif');"><IMG src="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_09.gif" width="77" height="23" name="_HPB_ROLLOVER1" border="0"></A></TD>
<TD width="3"><IMG src="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_frame_10.gif" width="3" height="23" alt=""></TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
</TBODY>
</TABLE>
</center>

EOF
}



	if ($next_num ne '') {

		while (($key,$val) = each %FORM2) {

			if ($key ne 'FF') { $buf = "$buf&$key=$val"; }
		}

print <<"EOF";

<!--Google Anaylytics：ここから-->
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-779505-5";
urchinTracker();
</script>
<!--Google Anaylytics：ここまで-->

</BODY>
</HTML>
EOF

exit;
	}
}

print <<"EOF";
<!--Google Anaylytics：ここから-->
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-779505-5";
urchinTracker();
</script>
<!--Google Anaylytics：ここまで-->
</BODY>
</HTML>
EOF

exit;


sub error {

	print "Content-type: text/html\n\n";
print "<html><head><title>$title</title></head>\n";
print "$body\n";
print "<h1>$_[0]</h1>\n";
	print "<h3>$_[1]</h3><p>\n";
	print "ブラウザの[戻る]ボタンを押して前の画面に移動してください.<p>\n";
print "</body></html>\n";
exit;
}
