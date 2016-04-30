#!/usr/bin/perl
#
# 簡易データベース v2.1 (SJIS)　検索用
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

#データベースファイル
#$file = "../text_data/special_tsutsuji.txt";

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
$ID = $FORM{'ID'};
$ID_T = $FORM{'ID_T'};
@add = ("../text_data/special_tsutsuji_",$ID,".txt"); $file = join("",@add);

if (!open(IN,$file)) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

foreach $num (0 .. $#BASE) {

$data = $data2 = $BASE[$num];
&jcode'convert(*data,'sjis');
($ID_T,$TITLE_T,$UY_T,$UM_T,$UD_T,$COM_T) = split(/\,/,$data);

# ID(一致)

if ($FORM{'ID_T'} ne 'all') {
if ($ID_T eq $FORM{'ID_T'}) { ; } else { next; }
}

# 検索終了処理
if ($hit == $page) { $next_num = $num; last; }
else { push(@NEW,$data2); $hit++; }
}

#■検索結果

($ID_T,$TITLE_T,$UY_T,$UM_T,$UD_T,$COM_T) = split(/\,/,$data);

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
HpbImgPreload('_HPB_ROLLOVER1', '../../images/0404tsutsuji_frame_09.gif', '../../images/0404tsutsuji_frame_over_09.gif');
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
<TD width="10"><IMG src="../../images/0404tsutsuji_frame_01.gif" width="10" height="29" alt=""></TD>
EOF

($ID_T,$TITLE_T,$UY_T,$UM_T,$UD_T,$COM_T) = split(/\,/,$data);
@add = ("../../images/special_tsutsuji/tsutsuji_",$ID_T,"w.jpg"); $grph01 = join("",@add);

print <<"EOF";
<TD background="../../images/0404tsutsuji_frame_02.gif"><B>薬王寺のツツジ：$UM_T月$UD_T日</B>
</TD>
<TD width="3"><IMG src="../../images/0404tsutsuji_frame_03.gif" width="3" height="29" alt=""></TD>
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
<TD background="../../images/0404tsutsuji_frame_04.gif" width="3"></TD>
<TD><IMG src="$grph01"></TD>
<TD width="3" background="../../images/0404tsutsuji_frame_06.gif"></TD>
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
<TD width="10"><IMG src="../../images/0404tsutsuji_frame_07.gif" width="10" height="23" alt=""></TD>
<TD background="../../images/0404tsutsuji_frame_08.gif"><font style="font-size:1px">.</font></TD>
<TD width="77"><A href="Javascript:window.close()" id="_HPB_ROLLOVER1" onmouseout="HpbImgSwap('_HPB_ROLLOVER1', '../../images/0404tsutsuji_frame_09.gif');" onmouseover="HpbImgSwap('_HPB_ROLLOVER1', '../../images/0404tsutsuji_frame_over_09.gif');"><IMG src="../../images/0404tsutsuji_frame_09.gif" width="77" height="23" name="_HPB_ROLLOVER1" border="0"></A></TD>
<TD width="3"><IMG src="../../images/0404tsutsuji_frame_10.gif" width="3" height="23" alt=""></TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
<tr> 
<td align="left">
<a href="http://www.hdg.jp/" target="_blank" title="インターネット広告"><strong>インターネット広告</strong></a> | <a href="http://www.feinauto.com/" target="_blank" title="ファインオート"><strong>ファインオート</strong></a> | <a href="http://www.rockets-tyc.com/" target="_blank" title="ロケッツ"><strong>ロケッツ</strong></a> | <a href="http://www.tsa1-midori.com/" target="_blank" title="タイヤ販売"><strong>タイヤ販売</strong></a>
</td>
</tr>
</TBODY>
</TABLE>
</center>
EOF
}
print <<"EOF";
<!--Google Anaylytics：ここから-->
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-779505-5");
pageTracker._trackPageview();
} catch(err) {}</script>
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
