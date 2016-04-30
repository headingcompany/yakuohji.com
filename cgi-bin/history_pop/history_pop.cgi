#!/usr/bin/perl
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

#データベースファイル
$file = "../text_data/history.txt";

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
if ($FORM{'ID'} ne 'all') {
if ($ID eq $FORM{'ID'}) { push(@NEW,$data2);  next;}
}

# 検索終了処理
push(@NEW1_2,$data2);

}


#■検索処理
sub symd {

if ($UY <= $year) {
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
else{ next; }
}

sub endymd {

if ($EY >= $year) {
if ($EM >= $mon) {
       if ($ED >= $day) { $pnew = 1; }
                        else {
                             if ($EM > $mon) { $pnew = 1; }
                                             else {
                                                  if ($EY > $year) { $pnew = 1; }
                                                  else { next; }
                                                  }
                             }
       }
       else{
           if ($EY > $year) { $pnew = 1; }
                             else { next; }
           }
}
else{ next; }

}


#■検索結果
foreach $data (@NEW) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$NO,$COM,$COM2,$ST,$URL,$NTITLE) = split(/\,/,$data);

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$TITLE / 七国山薬王寺</title>
<link rel="stylesheet" href="../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../rollover.js"></SCRIPT>
</head>

<body leftmargin="2" topmargin="2" rightmargin="2" marginwidth="2" marginheight="2" bgcolor="#ff6600">
<CENTER>
<TABLE border="0" width="310" cellpadding="0" cellspacing="0" bgcolor="#ffffff">
<TBODY>
<TR>
<TD width="5" height="5"><IMG src="../../images/history_backup_edge_01.gif" width="5" height="5" border="0"></TD>
<TD></TD>
<TD width="5" height="5"><IMG src="../../images/history_backup_edge_02.gif" width="5" height="5" border="0"></TD>
</TR>
<TR>
<TD></TD>
<TD>
EOF
if ($ST eq "1") { &main_his_url; }
else { ; }
print <<"EOF";
</TD>
<TD></TD>
</TR>
<TR>
<TD width="5" height="5"><IMG src="../../images/history_backup_edge_03.gif" width="5" height="5" border="0"></TD>
<TD></TD>
<TD width="5" height="5"><IMG src="../../images/history_backup_edge_04.gif" width="5" height="5" border="0"></TD>
</TR>
</TBODY>
</TABLE>
<table width="310" border="0" cellspacing="0" cellpadding="0">
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
</CENTER>
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
sub main_his_url {
open (IN,$URL);
while(<IN>){ print; }
close(IN);
}

exit;
