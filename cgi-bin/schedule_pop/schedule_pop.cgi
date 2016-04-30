#!/usr/bin/perl
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

#データベースファイル
$file = "../text_data/schedule.txt";

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

$UY2 = $FORM{'UY'};

#■検索処理

if (!open(IN,"$file")) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

$hit = 0;

foreach $num (0 .. $#BASE) {

$data = $data2 = $BASE[$num];
&jcode'convert(*data,'sjis');
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$data);
($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$mon++;
$year = $year + 1900;

&symd;

# UY(一致)
if ($FORM{'UY'} ne 'all') {
    if ($UY eq $FORM{'UY'}) { push(@NEW,$data2);  next;}
    }

# 検索終了処理
push(@NEW1_2,$data2);

}


#■検索処理
sub symd {

if ($mon <= 9) { @add = ("0",$mon); $mon = join("",@add); }
if ($day <= 9) { @add = ("0",$day); $day = join("",@add); }

if ($UY eq $year) {
if ($UM <= $mon) {
if ($UD <= $day) { &endymd; }
else {
if ($UM < $mon) { &endymd; }
else { next; }
}
}
else{
if ($UY < $year) { &endymd; }
else { next; }
}
}
elsif ($UY < $year) { &endymd; }
else{ next; }
}

sub endymd {

if ($EY >= $year) {
if ($EM >= $mon) {
if ($ED >= $day) { $pnew=1; }
else {
if ($EM > $mon) { $pnew=1; }
else {
if ($EY > $year) { $pnew=1; }
else { next; }
}
}
}
else{
if ($EY > $year) { $pnew=1; }
else { next; }
}
}
else{ next; }
}

#■検索結果
print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$UY2年の行事 / 七国山薬王寺</title>
<link rel="stylesheet" href="../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../rollover.js"></SCRIPT>
</head>

<body bgcolor="#ff6600">
<table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="ff9933">
<tr> 
<td width="5" height="5"><IMG src="../../images/edge_ff9944_ff6600_01.gif" width="5" height="5" border="0"></td>
<td><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
<td width="5" height="5"><IMG src="../../images/edge_ff9944_ff6600_02.gif" width="5" height="5" border="0"></td>
</tr>
<tr>
<td>&nbsp;</td>
<td><table width="100%" border="0" cellspacing="0" cellpadding="3">
<tr>
<td><strong><font color="ffffff">$UY2年の行事</font></strong></td>
</tr>
<tr>
<td><table width="100%" border="0" cellspacing="1" cellpadding="3">
<tr align="center" bgcolor="ffcc00"> 
<td><strong>日付</strong></td>
<td><strong>行事内容</strong></td>
</tr>
EOF
foreach $data (@NEW) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$data);
print <<"EOF";
<tr bgcolor="ffffff">
<td>$DATE</td>
<td>$COM</td>
</tr>
EOF
}
print <<"EOF";
</table></td>
</tr>
</table></td>
<td>&nbsp;</td>
</tr>
<tr>
<td width="5" height="5"><IMG src="../../images/edge_ff9944_ff6600_03.gif" width="5" height="5" border="0"></td>
<td><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
<td width="5" height="5"><IMG src="../../images/edge_ff9944_ff6600_04.gif" width="5" height="5" border="0"></td>
</tr>
</table>
<table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr>
<td align="center"><br>
<A href="Javascript:window.close()"><IMG src="../../images/close.gif" width="120" height="20" border="0"></A>
<hr size="1" color="ffffff"></td>
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
</body>
</html>
EOF

#URL表示ルーチン
sub ivent_st_url {
open (IN,$URL);
while(<IN>){ print; }
close(IN);
}

exit;
