#!/usr/bin/perl
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

#データベースファイル
$file = "../text_data/greet.txt";

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
&jcode'convert(*value,'sjis');

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

$hit = 0;
$next_num = '';

foreach $num (0 .. $#BASE) {

$data = $data2 = $BASE[$num];
&jcode'convert(*data,'sjis');
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$data);

# イベントID(一致)
if ($FORM{'ID'} ne 'all') {
if ($ID eq $FORM{'ID'}) { ; } else { next; }
}

# 検索終了処理
if ($hit == $page) { $next_num = $num; last; }
else { push(@NEW,$data2); $hit++; }

}

#■検索結果

foreach $data (@NEW) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$data);
@addupdate = ($UY,$UM,$UD); $update = join("",@addupdate);
@add = ("../../images/greeting_",$GEN,"_01.jpg"); $grph01 = join("",@add);
@add2 = ("../../images/greeting_",$GEN,"_",$update,"_02.jpg"); $grph02 = join("",@add2);
@add3 = ("../../images/greeting_",$GEN,"_03.jpg"); $grph03 = join("",@add3);
@add4 = ("../../images/greeting_",$GEN,"_04.gif"); $grph04 = join("",@add4);

print "Content-type: text/html\n\n";
print <<"EOF";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>ご挨拶：$TITLE / 七国山薬王寺</title>
<link rel="stylesheet" href="../../yakuohji_text.css" type="text/css">
</head>

<body bgcolor="#ff6600">
<div align="center">
<table border="0" cellpadding="0" cellspacing="0" bgcolor="ffffff">
<tr> 
<td width="5" height="5"><IMG src="../../images/history_backup_edge_01.gif" width="5" height="5" border="0"></td>
<td><font style="font-size:1px;line-height:1px">&nbsp;</font></td>
<td width="5" height="5"><IMG src="../../images/history_backup_edge_02.gif" width="5" height="5" border="0"></td>
</tr>
<tr> 
<td>&nbsp;</td>
<td>
<table width="300" border="0" cellpadding="0" cellspacing="0" bgcolor="ffffff">
<tr> 
<td height="5"><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
</tr>
<tr> 
<td><IMG src="$grph01" width="300" height="244" border="0"></td>
</tr>
<tr> 
<td><table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td valign="top"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td><img src="$grph02" width="229" height="42"></td>
</tr>
<tr> 
<td background="$grph04">
<table border="0" cellspacing="0" cellpadding="0">
<tr>
<td width="5">&nbsp;</td>
<td>$COM</td>
</tr>
<tr>
<td>
</td>
<td align="right"><hr height="1">（$UY/$UM/$UD掲載）</td>
</tr>
</table></td>
</tr>
</table></td>
<td width="71" valign="top"><IMG src="$grph03" width="71" height="152" border="0"></td>
</tr>
</table></td>
</tr>
<tr> 
<td height="5"><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
</tr>
</table></td>
<td>&nbsp;</td>
</tr>
<tr> 
<td width="5" height="5"><IMG src="../../images/history_backup_edge_03.gif" width="5" height="5" border="0"></td>
<td><font style="font-size:1px;line-height:1px">&nbsp;</font></td>
<td width="5" height="5"><IMG src="../../images/history_backup_edge_04.gif" width="5" height="5" border="0"></td>
</tr>
</table>
<table width="300" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td>&nbsp;</td>
</tr>
<tr>
<td align="center"><A href="Javascript:window.close()"><IMG src="../../images/close.gif" width="120" height="20" border="0"></A><br> 
<hr width="100%" size="1" color="#ffffff"></td>
</tr>
<tr> 
<td><div align="right"><font color="ffffff">copyright(c) yakuohji.</font></div></td>
</tr>
<tr> 
<td align="left">
<a href="http://www.hdg.jp/" target="_blank" title="インターネット広告"><strong>インターネット広告</strong></a> | <a href="http://www.feinauto.com/" target="_blank" title="ファインオート"><strong>ファインオート</strong></a> | <a href="http://www.rockets-tyc.com/" target="_blank" title="ロケッツ"><strong>ロケッツ</strong></a> | <a href="http://www.tsa1-midori.com/" target="_blank" title="タイヤ販売"><strong>タイヤ販売</strong></a>
</td>
</tr>
</table>
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
</div>
</body>
</html>
EOF
}

exit;
