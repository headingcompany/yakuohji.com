#!/usr/bin/perl
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

#データベースファイル
$file = "../text_data/ivent.txt";

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

foreach $num (0 .. $#BASE) {

$data = $data2 = $BASE[$num];
&jcode'convert(*data,'sjis');
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$data);
($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$mon++;
$year = $year + 1900;

&symd;

# イベントID(一致)
if ($hit eq "0") {
if ($ID eq $FORM{'ID'}) { push(@NEW,$data2);  $hit++; next;}
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
foreach $data (@NEW) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$data);

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>最新の行事：$TITLE / 七国山薬王寺</title>
<link rel="stylesheet" href="/common/css/yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="/common/js/rollover.js"></SCRIPT>
</head>

<body leftmargin="2" topmargin="2" rightmargin="2" marginwidth="2" marginheight="2" bgcolor="#ff6600">
<table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr>
<td><table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr>
<td width="110"><IMG SRC="../../images/ivent_01.gif" WIDTH=110 HEIGHT=15 ALT=""></td>
<td background="../../images/ivent_02.gif">&nbsp;</td>
<td width="60"><IMG SRC="../../images/ivent_03.gif" WIDTH=60 HEIGHT=15 ALT=""></td>
</tr>
</table></td>
</tr>
<tr>
<td><table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr>
<td width="10" background="../../images/ivent_04.gif">&nbsp;</td>
<td bgcolor="ffffff"> 
<table width="100%" border="0" cellspacing="0" cellpadding="3">
<tr>
<td><strong>$UY年$UM月$UD日：$TITLE</strong>
<hr size="1"></td>
</tr>
<tr>
<td>
EOF
if ($ST eq 1) { &ivent_st_url; }
else {
print <<"EOF";
<table border="0" cellspacing="0" cellpadding="3">
EOF
if ($GRPHNO eq 0) {
print <<"EOF";
<tr>
<td valign="top">$COM</td>
</tr>
EOF
}
else {
for ($hit = 1; $hit <= $GRPHNO; $hit++) {
@add = ("../../images/ivent/",$ID,"_",$hit,".jpg"); $GRPH01 = join("",@add);
if ($hit eq 2) {$COM = $COM2}
if ($hit eq 3) {$COM = $COM3}
print <<"EOF";
<tr>
<td valign="top">
<table border="0" cellpadding="0" cellspacing="1" bgcolor="000000">
<tr>
<td bgcolor="ffffff"><img src="$GRPH01" border="0"></td>
</tr>
</table></td>
<td valign="top">$COM</td>
</tr>
EOF
}
}
print <<"EOF";
</table>
EOF
}
print <<"EOF";
</td>
</tr>
<tr> 
<td>
<hr size="1">
<table border="0" cellpadding="0" cellspacing="2" bgcolor="ff6600">
<tr>
<td><strong><font color="ffffff">過去の行事</font></strong></td>
</tr>
<tr>
<td>
<table width="100%" border="0" cellspacing="1" cellpadding="3">
EOF
foreach $data (@NEW1_2) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$data);
print <<"EOF";
<tr>
<td bgcolor="ff9933">$UY/$UM/$UD</td>
<td bgcolor="ffffff"><a href="/event_$ID.html">$TITLE</a></td>
</tr>
EOF
}
print <<"EOF";
</table></td>
</tr>
</table>
</td>
</tr>
</table></td>
<td width="10" background="../../images/ivent_06.gif">&nbsp;</td>
</tr>
</table></td>
</tr>
<tr>
<td><table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr>
<td width="110"><IMG SRC="../../images/ivent_07.gif" WIDTH=110 HEIGHT=10 ALT=""></td>
<td background="../../images/ivent_08.gif"><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
<td width="60"><IMG SRC="../../images/ivent_09.gif" WIDTH=60 HEIGHT=10 ALT=""></td>
</tr>
</table></td>
</tr>
</table>
<table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr>
<td align="center"><br><A href="Javascript:window.close()"><IMG src="../../images/close.gif" width="120" height="20" border="0"></A> 
<hr size="1" color="ffffff"></td>
</tr>
<tr>
<td align="right"><font color="ffffff">copyright(c) yakuohji.</font></td>
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
}

#URL表示ルーチン
sub ivent_st_url {
open (IN,$URL);
while(<IN>){ print; }
close(IN);
}

exit;
