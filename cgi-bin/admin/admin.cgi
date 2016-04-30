#!/usr/bin/perl
#
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';
require './cgi-lib.pl';

#データベースファイル
$filetop = "../text_data/top.txt";
$fileivent = "../text_data/ivent.txt";
$filegreet = "../text_data/greet.txt";
$fileschedule = "../text_data/schedule.txt";

#-----------------------------------------------------------------------------------

#■入力

&ReadParse(*in);

$mode = $in{'mode'};
$UY = $in{'UY'};
$UM = $in{'UM'};
$UD = $in{'UD'};
$EY = $in{'EY'};
$EM = $in{'EM'};
$ED = $in{'ED'};
$TITLE = $in{'TITLE'};
$COM = $in{'COM'};

$ST = $in{'ST'};
$URL= $in{'URL'};

$COM2=$in{'COM2'};
$COM3=$in{'COM3'};

$File0 = $in{'File0'};
$File1 = $in{'File1'};
$File2 = $in{'File2'};
$File3 = $in{'File3'};

$GRPHNO = $in{'GRPHNO'};
$EXGRPHNO = $in{'EXGRPHNO'};

$NTITLE = $in{'NTITLE'};
$GEN = $in{'GEN'};
$DATE = $in{'DATE'};

$DELGRPH = $in{'DELGRPH'};

$GRPH = $in{'GRPH'};
$GRPH_F = $in{'GRPH_F'};


$DELID = $in{'DELID'};
$REID = $in{'REID'};


$data = '';

if ($in{'mode'} eq "top") { &top; exit; }
                       elsif ($in{'mode'} eq "topadd") { &topadd; exit; }
                       elsif ($in{'mode'} eq "topdel") { &topdel; exit; }
                       elsif ($in{'mode'} eq "topre")  { &topre; exit; }
                       elsif ($in{'mode'} eq "topreadd")  { &topreadd; exit; }

if ($in{'mode'} eq "ivent") { &ivent; exit; }
                       elsif ($in{'mode'} eq "iventadd") { &iventadd; exit; }
                       elsif ($in{'mode'} eq "iventdel") { &iventdel; exit; }
                       elsif ($in{'mode'} eq "iventre")  { &iventre; exit; }
                       elsif ($in{'mode'} eq "iventreadd")  { &iventreadd; exit; }


if ($in{'mode'} eq "greet") { &greet; exit; }
                       elsif ($in{'mode'} eq "greetadd") { &greetadd; exit; }
                       elsif ($in{'mode'} eq "greetdel") { &greetdel; exit; }
                       elsif ($in{'mode'} eq "greetre")  { &greetre; exit; }
                       elsif ($in{'mode'} eq "greetreadd")  { &greetreadd; exit; }


if ($in{'mode'} eq "schedule") { &schedule; exit; }
                       elsif ($in{'mode'} eq "scheduleadd") { &scheduleadd; exit; }
                       elsif ($in{'mode'} eq "scheduledel") { &scheduledel; exit; }
                       elsif ($in{'mode'} eq "schedulere")  { &schedulere; exit; }
                       elsif ($in{'mode'} eq "schedulereadd")  { &schedulereadd; exit; }


################################################################################

sub top {

open(FILE,$filetop);
@allbody = <FILE>;
close(FILE);


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>「お知らせ」管理画面 / 薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
  <table border="0" cellpadding="0" cellspacing="0">
    <tr> 
      <td height="34"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190">お知らせ</td>
            <td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">
          <tr> 
            <td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
            <td align="center" valign="top">
<form enctype="multipart/form-data" action="./admin.cgi" method="GET">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>掲載終了年</td><td><SELECT name="EY" tabindex="4">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="5">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="6">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="7"></td></tr>
<tr><td>コメント</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="8"></TEXTAREA></td></tr>
<tr><td colspan="2" align="center"><input type="hidden" name="mode" value="topadd"><input type="submit" value="追加" tabindex="11"><input type="reset" value="リセット" tabindex="12"></td></tr>
</table>
</form>
<br>
<table border="1">
<tr>
<td>ID</td>
<td>TITLE</td>
<td>UY</td>
<td>UM</td>
<td>UD</td>
<td>EY</td>
<td>EM</td>
<td>ED</td>
<td>COM</td>
<td></td>
<td></td>
</tr>
EOF
foreach $line (@allbody) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM) = split(/\,/,$line);
print <<"EOF";
<tr>
<td>$ID</td>
<td>$TITLE</td>
<td>$UY</td>
<td>$UM</td>
<td>$UD</td>
<td>$EY</td>
<td>$EM</td>
<td>$ED</td>
<td>$COM</td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="DELID" value="$ID"><input type="hidden" name="mode" value="topdel"><input type="submit" value="削除"></form></td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="REID" value="$ID"><input type="hidden" name="mode" value="topre"><input type="submit" value="変更"></form></td>
</tr>

EOF
}

print <<"EOF";
</table></td>
            <td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td height="15"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
            <td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
          </tr>
        </table></td>
    </tr>
  </table>
</div>
</body>
</html>


EOF

}


sub topadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }

@add = ($UY,$UM,$UD);
$IDADD = join("",@add);

$COM =~ s/\n/<br>/g;

open(FILE,">>$filetop");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM\n";
close(FILE);

open(FILE,"<$filetop");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$filetop");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~ s/ //g;
 $sortadd =~ s///g;
 $sortadd =~ s/\\r\n//g; $sortadd =~ s/\\n//g; $sortadd =~ s/\\r//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$filetop");
@allbody = <FILE>;
close(FILE);

foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }
}

open(FILE,">$filetop");
print FILE @allbody;
close(FILE);


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">登録しました。<br>
<input type="button" value="戻る" onclick="history.back()">
</body>
</html>

EOF

}
exit;




sub topdel {

open(FILE,"<$filetop");
@allbody = <FILE>;
close(FILE);

foreach $line(@allbody){
 if ($line =~ /$DELID/){
                    $line =~ s/.*\n//;
                    }
}

open(FILE,">$filetop");
print FILE @allbody;
close(FILE);

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
削除しました。<br>
<input type="button" value="戻る" onclick="history.back()">

</body>
</html>

EOF

}

sub topre {

open(FILE,$filetop);
@allbody = <FILE>;
close(FILE);
$hit = 0;

foreach $num (0 .. $#allbody) {

	$line = $line2 = $allbody[$num];
	&jcode'convert(*line,'sjis');
        ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM) = split(/\,/,$line);

	# 変更ID(一致)

	if ($REID ne 'all') {

		if ($ID eq $REID) { ; } else { next; }
	}


	# 検索終了処理
	if ($hit == 1) { last; }
	else { push(@NEW,$line2); $hit++; }
}

print "Content-type: text/html\n\n";
print <<"EOF";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
  <table border="0" cellpadding="0" cellspacing="0">
    <tr> 
      <td height="34"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190">お知らせ</td>
            <td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">
          <tr> 
            <td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
            <td align="center" valign="top">
EOF
foreach $line (@NEW) {
        ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM) = split(/\,/,$line);
$COM =~ s/<br>/\n/g;

print <<"EOF";
<form enctype="multipart/form-data" action="./admin.cgi" method="POST">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="$UY" selected>$UY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="$UM" selected>$UM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="$UD" selected>$UD</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>掲載終了年</td><td><SELECT name="EY" tabindex="4">
 <OPTION value="$EY" selected>$EY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="5">
 <OPTION value="$EM" selected>$EM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="6">
 <OPTION value="$ED" selected>$ED</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="7" value="$TITLE"></td></tr>
<tr><td>コメント</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="8">$COM</TEXTAREA></td></tr>
<tr><td colspan="2" align="center"><input type="hidden" name="mode" value="topreadd"><input type="hidden" name="REID" value="$ID"><input type="submit" value="変更" tabindex="9"></td></tr>
</table>
</form>
EOF
}
print <<"EOF";
<input type="button" value="戻る" onclick="history.back()">
</td>
            <td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td height="15"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
            <td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
          </tr>
        </table></td>
    </tr>
  </table>
</div>
</body>
</html>


EOF

}


sub topreadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }

@add = ($UY,$UM,$UD);
$IDADD = join("",@add);

$COM =~ s/\n/\<br\>/g;


open(FILE,"<$filetop");
@allbody = <FILE>;
close(FILE);

foreach $line(@allbody){
 if ($line =~ /$REID/){
                    $line =~ s/.*\n//;
                    }
}

open(FILE,">$filetop");
print FILE @allbody;
close(FILE);

open(FILE,">>$filetop");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM\n";
close(FILE);

open(FILE,"<$filetop");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$filetop");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~s/ //g;
 $sortadd =~s///g;
 $sortadd =~s/\\n//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$filetop");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }
}

open(FILE,">$filetop");
print FILE @allbody;
close(FILE);




print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
更新しました。<br>
<input type="button" value="戻る" onclick="history.go(-2)">

</body>
</html>

EOF

}



################################################################################

sub ivent {

open(FILE,$fileivent);
@allbody = <FILE>;
close(FILE);


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
<table border="0" cellspacing="0" cellpadding="0">
<tr> 
<td><table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td width="190">最新の行事</td>
<td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
<td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
</tr>
</table></td>
</tr>
<tr> 
<td><table width="100%" border="0" cellpadding="0" cellspacing="0">
<tr> 
<td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
<td align="center">
<form enctype="multipart/form-data" action="./admin.cgi" method="POST">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td>
<td>掲載終了年</td><td><SELECT name="EY" tabindex="4">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="9999">9999</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="5">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="6">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="7" value="$TITLE"></td><td>インデックス写真データ</td><td><input type="FILE" name="File0" accept="image/jpeg" size="30" tabindex="8"></td>
</tr>
<tr>
  <td>写真データ1</td><td><input type="FILE" name="File1" accept="image/jpeg" size="30" tabindex="8"></td>
  <td>コメント1</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="9"></TEXTAREA></td>
</tr>
<tr>
  <td>写真データ2</td><td><input type="FILE" name="File2" accept="image/jpeg" size="30" tabindex="10"></td>
  <td>コメント2</td><td><TEXTAREA name="COM2" rows="5" cols="30" tabindex="11"></TEXTAREA></td>
</tr>
<tr>
  <td>写真データ3</td><td><input type="FILE" name="File3" accept="image/jpeg" size="30" tabindex="12"></td>
  <td>コメント3</td><td><TEXTAREA name="COM3" rows="5" cols="30" tabindex="13"></TEXTAREA></td>
</tr>
<tr>
  <td>利用データ</td><td><SELECT name="ST" tabindex="14"><OPTION value="0" selected>データから生成</OPTION><OPTION value="1">htmlを利用</OPTION></select></td><td>htmlデータ位置</td><td><input type="text" name="TITLE" size="30" tabindex="15" value="$URL"></td>
</tr>
<tr><td colspan="4" align="center"><input type="hidden" name="mode" value="iventadd"><input type="submit" value="追加" tabindex="16"><input type="reset" value="リセット" tabindex="17"></td></tr>
</table>
</form>
<br>
<table border="1">
<td>ID</td>
<td>TITLE</td>
<td>UY</td>
<td>UM</td>
<td>UD</td>
<td>EY</td>
<td>EM</td>
<td>ED</td>
<td>COM</td>
<td>ST</td>
<td>URL</td>
<td>GRPHNO</td>
<td>COM2</td>
<td>COM3</td>
<td></td>
<td></td>
</tr>
EOF
foreach $line (@allbody) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$line);

print <<"EOF";

<tr>
<td>$ID</td>
<td>$TITLE</td>
<td>$UY</td>
<td>$UM</td>
<td>$UD</td>
<td>$EY</td>
<td>$EM</td>
<td>$ED</td>
<td>$COM</td>
<td>$ST</td>
<td>$URL</td>
<td>$GRPHNO</td>
<td>$COM2</td>
<td>$COM3</td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="DELID" value="$ID"><input type="hidden" name="GRPHNO" value="$GRPHNO"><input type="hidden" name="mode" value="iventdel"><input type="submit" value="削除"></form></td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="REID" value="$ID"><input type="hidden" name="mode" value="iventre"><input type="submit" value="変更"></form></td>
</tr>

EOF
}

print <<"EOF";
</table></td>
<td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
</tr>
</table></td>
</tr>
<tr> 
<td> <table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
<td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
<td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
</tr>
</table></td>
</tr>
</table>
</div>
</body>
</html>

EOF
}


sub iventadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }
if ($ST eq '1') {
  if ($URL eq '') { &error; }
}

if ($File1 ne "") { $GRPHNO = 1; }
if ($File2 ne "") { $GRPHNO = 2; }
if ($File3 ne "") { $GRPHNO = 3; }

if ($File1 eq "") { $GRPHNO = 0; }


@add = ($UY,$UM,$UD); $IDADD = join("",@add);
$COM =~ s/\n/<br>/g; $COM2 =~ s/\n/<br>/g; $COM3 =~ s/\n/<br>/g;

open(FILE,">>$fileivent");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3\n";
close(FILE);

open(FILE,"<$fileivent");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$fileivent");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~ s/ //g;
 $sortadd =~ s///g;
 $sortadd =~ s/\\r\n//g; $sortadd =~ s/\\n//g; $sortadd =~ s/\\r//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$fileivent");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }

}

open(FILE,">$fileivent");
print FILE @allbody;;
close(FILE);


  @file1names = split /\\/,$incfn{'File0'};
  $file1name = $file1names[-1];
#ファイル拡張子を取り出す。
  @file1types = split /\./,$file1name;
  $file1type = $file1types[-1];
#ファイルを指定ディレクトリに保存
  open (OUT, ">../../../images/yakuohji/ivent/" . "$IDADD" . "s" . '.' . "$file1type");
  binmode (OUT);
  print (OUT $File0);
  close (OUT);

for ($i=1;$i<=$GRPHNO;$i++) {
  if ($i eq "1") { @file1names = split /\\/,$incfn{'File1'}; }
  if ($i eq "2") { @file1names = split /\\/,$incfn{'File2'}; }
  if ($i eq "3") { @file1names = split /\\/,$incfn{'File3'}; }
#ファイル名を取り出します。
#  @file1names = split /\\/,$incfn{'File1'};
  $file1name = $file1names[-1];
#ファイル拡張子を取り出す。
  @file1types = split /\./,$file1name;
  $file1type = $file1types[-1];
#ファイルを指定ディレクトリに保存
  open (OUT, ">../../../images/yakuohji/ivent/" . "$IDADD" . "_" . "$i". '.' . "$file1type");
  binmode (OUT);
    if ($i eq "1") { print (OUT $File1); }
    if ($i eq "2") { print (OUT $File2); }
    if ($i eq "3") { print (OUT $File3); }
  close (OUT);
}

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">登録しました。<br>
<input type="button" value="戻る" onclick="history.back()">
</body>
</html>

EOF

}




sub iventdel {

open(FILE,"<$fileivent");
@allbody = <FILE>;
close(FILE);

foreach $line(@allbody){
                       if ($line =~ /$DELID/){
                                             $line =~ s/.*\n//;
                                             }
                       }

open(FILE,">$fileivent");
print FILE @allbody;
close(FILE);

$fileiventG = unlink("../../../images/yakuohji/ivent/$DELID" . "s" . ".jpg");
print $fileiventG;

for ($i=1;$i<=$GRPHNO;$i++) {
$fileiventG = unlink("../../../images/yakuohji/ivent/$DELID" . "_" . "$i" . ".jpg");
print $fileiventG;
}

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
削除しました。<br>
<input type="button" value="戻る" onclick="history.back()">

</body>
</html>

EOF

}

sub iventre {

open(FILE,$fileivent);
@allbody = <FILE>;
close(FILE);
$hit = 0;

foreach $num (0 .. $#allbody) {

	$line = $line2 = $allbody[$num];
	&jcode'convert(*line,'sjis');
        ($ID,$UPY,$UPM,$UPD,$MENU,$CL,$MATE,$COM) = split(/\,/,$line);

	# 変更ID(一致)

	if ($REID ne 'all') {

		if ($ID eq $REID) { ; } else { next; }
	}


	# 検索終了処理
	if ($hit == 1) { last; }
	else { push(@NEW,$line2); $hit++; }
}


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
<table border="0" cellspacing="0" cellpadding="0">
<tr> 
<td><table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td width="190">最新の行事</td>
<td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
<td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
</tr>
</table></td>
</tr>
<tr> 
<td>
EOF
foreach $line (@NEW) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$line);
$COM =~ s/<br>/\n/g;
$COM2 =~ s/<br>/\n/g;
$COM3 =~ s/\n//g;
$COM3 =~ s/<br>/\n/g;

if ($ST eq "0") { $ST1 = "データから生成" }
  elsif ($ST eq "1") { $ST1 = "htmlデータ利用" }

@add = ("../../../images/yakuohji/ivent/",$ID,"s.jpg"); $GRPHs = join("",@add);

for ($i=0;$i<=GRPHNO;$i++) {
  if ($GRPHNO >= "1") { @add = ("../../../images/yakuohji/ivent/",$ID,"_1.jpg"); $GRPH1 = join("",@add); }
  if ($GRPHNO >= "2") { @add = ("../../../images/yakuohji/ivent/",$ID,"_2.jpg"); $GRPH2 = join("",@add); }
  if ($GRPHNO eq "3") { @add = ("../../../images/yakuohji/ivent/",$ID,"_3.jpg"); $GRPH3 = join("",@add); }
}
print <<"EOF";
<table width="100%" border="0" cellpadding="0" cellspacing="0">
<tr> 
<td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
<td align="center">

<form enctype="multipart/form-data" action="./admin.cgi" method="POST">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="$UY" selected>$UY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="$UM" selected>$UM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="$UD" selected>$UD</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td>
<td>掲載終了年</td><td><SELECT name="EY" tabindex="4">
 <OPTION value="$EY" selected>$EY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="5">
 <OPTION value="$EM" selected>$EM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="6">
 <OPTION value="$ED" selected>$ED</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="7" value="$TITLE"></td><td>インデックス写真データ</td><td><input type="FILE" name="File0" accept="image/jpeg" size="30" tabindex="8">
EOF
if ($GRPHNO ne "0") {
print <<"EOF";
<table border="1">
<tr>
<td><IMG SRC="$GRPHs"></td>
</tr>
</table>
EOF
}
print <<"EOF";
</td>
</tr>
<tr>
  <td>写真データ1</td><td><input type="FILE" name="File1" accept="image/jpeg" size="30" tabindex="8">
EOF
if ($GRPHNO >= 1) {
print <<"EOF";
<table border="1">
<tr>
<td><IMG SRC="$GRPH1"></td>
</tr>
</table>
EOF
}
print <<"EOF";
</td>
  <td>コメント1</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="9">$COM</TEXTAREA></td>
</tr>
<tr>
  <td>写真データ2</td><td><input type="FILE" name="File2" accept="image/jpeg" size="30" tabindex="10">
EOF
if ($GRPHNO >= 2) {
print <<"EOF";
<table border="1">
<tr>
<td><IMG SRC="$GRPH2"></td>
</tr>
EOF
  if ($GRPHNO eq 2) {
print <<"EOF";
<tr><td><table><td><b>削除ボタン</b><br>削除は下から順番におこないます</td><td><input type="checkbox" name="DELGRPH" value="G2"></td></table></td></tr>
EOF
  }
print <<"EOF";
</table>
EOF
}
print <<"EOF";
</td>
  <td>コメント2</td><td><TEXTAREA name="COM2" rows="5" cols="30" tabindex="11">$COM2</TEXTAREA></td>
</tr>
<tr>
  <td>写真データ3</td><td><input type="FILE" name="File3" accept="image/jpeg" size="30" tabindex="12">
EOF
if ($GRPHNO eq "3") {
print <<"EOF";
<table border="1">
<tr>
<td><IMG SRC="$GRPH3"></td>
</tr>
EOF
  if ($GRPHNO eq 3) {
print <<"EOF";
<tr><td><table><td><b>削除ボタン</b><br>削除は下から順番におこないます</td><td><input type="checkbox" name="DELGRPH" value="G3"></td></table></td></tr>
EOF
  }
print <<"EOF";
</table>
EOF
}
print <<"EOF";
</td>
  <td>コメント3</td><td><TEXTAREA name="COM3" rows="5" cols="30" tabindex="13">$COM3</TEXTAREA></td>
</tr>
<tr>
  <td>利用データ</td><td><SELECT name="ST" tabindex="14"><OPTION value="$ST" selected>$ST1</OPTION><OPTION value="0">データから生成</OPTION><OPTION value="1">htmlを利用</OPTION></select></td><td>htmlデータ位置</td><td><input type="text" name="TITLE" size="30" tabindex="15" value="$URL"></td>
</tr>
<tr><td colspan="4" align="center"><input type="hidden" name="mode" value="iventreadd"><input type="hidden" name="REID" value="$ID"><input type="hidden" name="EXGRPHNO" value="$GRPHNO"><input type="submit" value="変更" tabindex="16"><input type="reset" value="リセット" tabindex="17"></td></tr>
</table>
</form>

<br>



EOF
}
print <<"EOF";



</td>
<td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
</tr>
</table></td>
</tr>
<tr> 
<td> <table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
<td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
<td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
</tr>
</table></td>
</tr>
</table>
</div>
</body>
</html>

EOF
}


sub iventreadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }
if ($ST eq '1') { if ($URL eq '') { &error; } }

$COM =~ s/\n/<br>/g;
$COM2 =~ s/\n/<br>/g;
$COM3 =~ s/\n/<br>/g;

@add = ($UY,$UM,$UD); $IDADD = join("",@add);

@add = ("../../../images/yakuohji/ivent/",$IDADD,"s.jpg");  $GRPHs = join("",@add);
@add = ("../../../images/yakuohji/ivent/",$REID,"s.jpg");   $GRPHsRE = join("",@add);
@add = ("../../../images/yakuohji/ivent/",$IDADD,"_1.jpg"); $GRPH1 = join("",@add);
@add = ("../../../images/yakuohji/ivent/",$REID,"_1.jpg");  $GRPH1RE = join("",@add);
@add = ("../../../images/yakuohji/ivent/",$IDADD,"_2.jpg"); $GRPH2 = join("",@add);
@add = ("../../../images/yakuohji/ivent/",$REID,"_2.jpg");  $GRPH2RE = join("",@add);
@add = ("../../../images/yakuohji/ivent/",$IDADD,"_3.jpg"); $GRPH3 = join("",@add);
@add = ("../../../images/yakuohji/ivent/",$REID,"_3.jpg");  $GRPH3RE = join("",@add);


if ($IDADD eq $REID) {
  if ($File0 ne '') { $CGRPH=0; &iventgrph; $GRPHNO = $EXGRPHNO; }
  if ($File1 ne '') { $CGRPH=1; &iventgrph; &grphno_c; }
  if ($File2 ne '') { $CGRPH=2; &iventgrph; &grphno_c; }
  if ($File3 ne '') { $CGRPH=3; &iventgrph; &grphno_c; }

  if ($File0 ne '') { ; }
    elsif ($File1 ne '') { ; }
    elsif ($File2 ne '') { ; }
    elsif ($File3 ne '') { ; }
    else { $GRPHNO = $EXGRPHNO; }

}
else {
  if ($File0 eq '') {
    $fileiventG = rename($GRPHsRE,$GRPHs);
    print $fileiventG;
  }
  else {
    $fileiventG = unlink($GRPHsRE);
    print $fileiventG;
    $CGRPH=0;
    &iventgrph;
  }
  if ($File1 eq '') {
    $fileiventG = rename($GRPH1RE,$GRPH1);
    print $fileiventG;
  }
  else {
    $fileiventG = unlink($GRPH1RE);
    print $fileiventG;
    $CGRPH=1;
    &iventgrph;
    &grphno_c;
  }
  if ($File2 eq '') {
    $fileiventG = rename($GRPH2RE,$GRPH2);
    print $fileiventG;
  }
  else {
    $fileiventG = unlink($GRPH2RE);
    print $fileiventG;
    $CGRPH=2;
    &iventgrph;
    &grphno_c;
  }
  if ($File3 eq '') {
    $fileiventG = rename($GRPH3RE,$GRPH3);
    print $fileiventG;
  }
  else {
    $fileiventG = unlink($GRPH3RE);
    print $fileiventG;
    $CGRPH=3;
    &iventgrph;
    &grphno_c;
  }
}


if ($DELGRPH eq "G2") { $fileiventG = unlink($GRPH2RE); print $fileiventG; $GRPHNO = 1; }
if ($DELGRPH eq "G3") { $fileiventG = unlink($GRPH3RE); print $fileiventG; $GRPHNO = 2; }


open(FILE,"<$fileivent");
@allbody = <FILE>;
close(FILE);

foreach $line(@allbody){
 if ($line =~ /$REID/){
                    $line =~ s/.*\n//;
                    }
}

open(FILE,">$fileivent");
print FILE @allbody;
close(FILE);

open(FILE,">>$fileivent");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3\n";
close(FILE);

open(FILE,"<$fileivent");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$fileivent");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~s/ //g;
 $sortadd =~s///g;
 $sortadd =~s/\\n//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$fileivent");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }
}

open(FILE,">$fileivent");
print FILE @allbody;
close(FILE);



print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
更新しました。<br>
<input type="button" value="戻る" onclick="history.go(-2)">

</body>
</html>
EOF
}

sub iventgrph {

if ($CGRPH eq 0) {
  #ファイル名を取り出します。
  @file1names = split /\\/,$incfn{'File0'};
  $file1name = $file1names[-1];
  #ファイル拡張子を取り出す。
  @file1types = split /\./,$file1name;
  $file1type = $file1types[-1];
  #ファイルを指定ディレクトリに保存
  open (OUT, ">$GRPHs");
  binmode (OUT);
  print (OUT $File0);
  close (OUT);
}

if ($CGRPH eq 1) {
  #ファイル名を取り出します。
  @file1names = split /\\/,$incfn{'File1'};
  $file1name = $file1names[-1];
  #ファイル拡張子を取り出す。
  @file1types = split /\./,$file1name;
  $file1type = $file1types[-1];
  #ファイルを指定ディレクトリに保存
  open (OUT, ">$GRPH1");
  binmode (OUT);
  print (OUT $File1);
  close (OUT);
}

if ($CGRPH eq 2) {
  #ファイル名を取り出します。
  @file1names = split /\\/,$incfn{'File2'};
  $file1name = $file1names[-1];
  #ファイル拡張子を取り出す。
  @file1types = split /\./,$file1name;
  $file1type = $file1types[-1];
  #ファイルを指定ディレクトリに保存
  open (OUT, ">$GRPH2");
  binmode (OUT);
  print (OUT $File2);
  close (OUT);
}

if ($CGRPH eq 3) {
  #ファイル名を取り出します。
  @file1names = split /\\/,$incfn{'File3'};
  $file1name = $file1names[-1];
  #ファイル拡張子を取り出す。
  @file1types = split /\./,$file1name;
  $file1type = $file1types[-1];
  #ファイルを指定ディレクトリに保存
  open (OUT, ">$GRPH3");
  binmode (OUT);
  print (OUT $File3);
  close (OUT);
}

}

sub grphno_c {

  if ($EXGRPHNO ne $CGRPH) {
    if ($CGRPH < $EXGRPHNO) { $GRPHNO = $EXGRPHNO; }
      else { $GRPHNO = $CGRPH; }
  }

}

################################################################################

sub greet {

open(FILE,$filegreet);
@allbody = <FILE>;
close(FILE);


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
  <table border="0" cellpadding="0" cellspacing="0">
    <tr> 
      <td height="34"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190">住職のあいさつ</td>
            <td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">
          <tr> 
            <td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
            <td align="center" valign="top">
<form enctype="multipart/form-data" action="./admin.cgi" method="POST">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>掲載終了年</td><td><SELECT name="EY" tabindex="4">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="5">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="6">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr>
  <td>記入者</td>
  <td>
    <SELECT name="GEN" tabindex="7">
      <OPTION value="" selected></OPTION>
      <OPTION value="22">第22世・光史</OPTION>
      <OPTION value="23">第23世・光正</OPTION>
      <OPTION value="24">第24世・貴志</OPTION>
    </SELECT>
  </td>
</tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="8"></td></tr>
<tr>
  <td>タイトル画像データ</td><td><input type="FILE" name="File1" accept="image/jpeg" size="30" tabindex="8">
</tr>
<tr><td>コメント</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="9"></TEXTAREA></td></tr>
<tr><td>次回のタイトル</td><td><input type="text" name="NTITLE" size="30" tabindex="10"></td></tr>
<tr><td colspan="2" align="center"><input type="hidden" name="mode" value="greetadd"><input type="submit" value="追加" tabindex="11"><input type="reset" value="リセット" tabindex="12"></td></tr>
</table>
</form>
<br>
<table border="1">
<tr>
<td>ID</td>
<td>TITLE</td>
<td>UY</td>
<td>UM</td>
<td>UD</td>
<td>EY</td>
<td>EM</td>
<td>ED</td>
<td>COM</td>
<td>GEN</td>
<td>NTITLE</td>
<td></td>
<td></td>
</tr>
EOF
foreach $line (@allbody) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$line);

print <<"EOF";

<tr>
<td>$ID</td>
<td>$TITLE</td>
<td>$UY</td>
<td>$UM</td>
<td>$UD</td>
<td>$EY</td>
<td>$EM</td>
<td>$ED</td>
<td>$COM</td>
<td>$GEN</td>
<td>$NTITLE</td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="DELID" value="$ID"><input type="hidden" name="GEN" value="$GEN"><input type="hidden" name="mode" value="greetdel"><input type="submit" value="削除"></form></td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="REID" value="$ID"><input type="hidden" name="mode" value="greetre"><input type="submit" value="変更"></form></td>
</tr>

EOF
}

print <<"EOF";
</table></td>
            <td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td height="15"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
            <td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
          </tr>
        </table></td>
    </tr>
  </table>
</div>
</body>
</html>


EOF

}


sub greetadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }
if ($GEN eq '') { &error; }
if ($NTITLE eq '') { &error; }


@add = ($UY,$UM,$UD); $IDADD = join("",@add);
@add = ("../../../images/yakuohji/greeting_",$GEN,"_",$IDADD,"_02.jpg"); $GRPH1 = join("",@add);

$COM =~ s/\n/<br>/g;

open(FILE,">>$filegreet");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE\n";
close(FILE);

#ファイル名を取り出します。
@file1names = split /\\/,$incfn{'File1'};
$file1name = $file1names[-1];
#ファイル拡張子を取り出す。
@file1types = split /\./,$file1name;
$file1type = $file1types[-1];
#ファイルを指定ディレクトリに保存
open (OUT, ">$GRPH1");
binmode (OUT);
print (OUT $File1);
close (OUT);


open(FILE,"<$filegreet");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$filegreet");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~ s/ //g;
 $sortadd =~ s///g;
 $sortadd =~ s/\\r\n//g; $sortadd =~ s/\\n//g; $sortadd =~ s/\\r//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$filegreet");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }

}

open(FILE,">$filegreet");
print FILE @allbody;;
close(FILE);

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">登録しました。<br>
<input type="button" value="戻る" onclick="history.back()">
</body>
</html>

EOF

}
exit;




sub greetdel {

open(FILE,"<$filegreet");
@allbody = <FILE>;
close(FILE);

@add = ("../../../images/yakuohji/greeting_",$GEN,"_",$DELID,"_02.jpg"); $GRPH1 = join("",@add);

$fileiventG = unlink("$GRPH1");
print $fileiventG;

foreach $line(@allbody){
 if ($line =~ /$DELID/){
$line =~ s/.*\n//;
}
 }
open(FILE,">$filegreet");
print FILE @allbody;
close(FILE);

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
削除しました。<br>
<input type="button" value="戻る" onclick="history.back()">

</body>
</html>

EOF

}

sub greetre {

open(FILE,$filegreet);
@allbody = <FILE>;
close(FILE);

foreach $num (0 .. $#allbody) {

	$line = $line2 = $allbody[$num];
	&jcode'convert(*line,'sjis');
        ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$line);

	# 変更ID(一致)

	if ($REID ne 'all') {

		if ($ID eq $REID) { ; } else { next; }
	}


	# 検索終了処理
	if ($hit == 1) { last; }
	else { push(@NEW,$line2); $hit++; }
}


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
  <table border="0" cellpadding="0" cellspacing="0">
    <tr> 
      <td height="34"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190">住職のあいさつ</td>
            <td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">
          <tr> 
            <td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
            <td align="center" valign="top">
EOF
foreach $line (@NEW) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$line);
$COM =~ s/<br>/\n/g;
if ($GEN eq "22") { $GEN2 = "第22世・光史"; }
  elsif ($GEN eq "23") { $GEN2 = "第23世・光正"; }
  elsif ($GEN eq "24") { $GEN2 = "第24世・貴志"; }

@add = ("../../../images/yakuohji/greeting_",$GEN,"_",$ID,"_02.jpg"); $GRPH1 = join("",@add);

print <<"EOF";
<form enctype="multipart/form-data" action="./admin.cgi" method="POST">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="$UY" selected>$UY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="$UM" selected>$UM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="$UD" selected>$UD</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>掲載終了年</td><td><SELECT name="EY" tabindex="1">
 <OPTION value="$EY" selected>$EY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="2">
 <OPTION value="$EM" selected>$EM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="3">
 <OPTION value="$ED" selected>$ED</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr>
  <td>記入者</td>
  <td>
    <SELECT name="GEN" tabindex="7">
      <OPTION value="$GEN" selected>$GEN2</OPTION>
      <OPTION value="22">第22世・光史</OPTION>
      <OPTION value="23">第23世・光正</OPTION>
      <OPTION value="24">第24世・貴志</OPTION>
    </SELECT>
  </td>
</tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="8" value="$TITLE"></td></tr>
<tr><td>コメント</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="9">$COM</TEXTAREA></td></tr>
<tr>
  <td>タイトル画像データ</td><td><input type="FILE" name="File1" accept="image/jpeg" size="30" tabindex="8">
<table border="1">
<tr>
<td><IMG SRC="$GRPH1"></td>
</tr>
</table>
</td>
</tr>
<tr><td>次回のタイトル</td><td><input type="text" name="NTITLE" size="30" tabindex="10" value="$NTITLE"></td></tr>
<tr><td colspan="2" align="center"><input type="hidden" name="mode" value="greetreadd"><input type="hidden" name="REID" value="$ID"><input type="submit" value="変更" tabindex="8"></td></tr>
</table>
</form>
<br>
<input type="reset" value="戻る" onclick="history.back()" tabindex="10">
EOF
}
print <<"EOF";
</td>
            <td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td height="15"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
            <td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
          </tr>
        </table></td>
    </tr>
  </table>
</div>
</body>
</html>


EOF

}


sub greetreadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }
if ($GEN eq '') { &error; }
if ($NTITLE eq '') { &error; }

@add = ($UY,$UM,$UD); $IDADD = join("",@add);
@add = ("../../../images/yakuohji/greeting_",$GEN,"_",$IDADD,"_02.jpg"); $GRPHADD = join("",@add);
@add = ("../../../images/yakuohji/greeting_",$GEN,"_",$REID,"_02.jpg"); $GRPHRE = join("",@add);

$COM =~ s/\n/\<br\>/g;

if ($IDADD eq $REID) { if ($File1 ne '') { &greetgrph; } }
  else {
      if ($File1 eq '') {
        $fileiventG = rename($GRPHRE,$GRPHADD);
        print $fileiventG;
      }
        else {
          $fileiventG = unlink($GRPHRE);
          print $fileiventG;
          &greetgrph;
        }
    }

open(FILE,"<$filegreet");
@allbody = <FILE>;
close(FILE);

foreach $line(@allbody){
 if ($line =~ /$REID/){
                    $line =~ s/.*\n//;
                    }
}

open(FILE,">$filegreet");
print FILE @allbody;
close(FILE);



open(FILE,">>$filegreet");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE\n";
close(FILE);

open(FILE,"<$filegreet");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$filegreet");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~s/ //g;
 $sortadd =~s///g;
 $sortadd =~s/\\n//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$filegreet");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }
}

open(FILE,">$filegreet");
print FILE @allbody;
close(FILE);




print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
更新しました。<br>
<input type="button" value="戻る" onclick="history.go(-2)">

</body>
</html>

EOF

}


sub greetgrph{
#ファイル名を取り出します。
@file1names = split /\\/,$incfn{'File1'};
$file1name = $file1names[-1];
#ファイル拡張子を取り出す。
@file1types = split /\./,$file1name;
$file1type = $file1types[-1];
#ファイルを指定ディレクトリに保存
open (OUT, ">$GRPHADD");
binmode (OUT);
print (OUT $File1);
close (OUT);
}



################################################################################

sub schedule {

open(FILE,$fileschedule);
@allbody = <FILE>;
close(FILE);


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
  <table border="0" cellpadding="0" cellspacing="0">
    <tr> 
      <td height="34"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190">行事日程</td>
            <td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">
          <tr> 
            <td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
            <td align="center" valign="top">
<form enctype="multipart/form-data" action="./admin.cgi" method="POST">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>終了年</td><td><SELECT name="EY" tabindex="1">
 <OPTION value="" selected></OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="2">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="3">
 <OPTION value="" selected></OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="4"></td></tr>
<tr><td>コメント</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="7"></TEXTAREA></td></tr>
<tr><td>日付</td><td><input type="text" name="DATE" size="30" tabindex="4"></td></tr>
<tr><td colspan="2" align="center"><input type="hidden" name="mode" value="scheduleadd"><input type="submit" value="追加" tabindex="8"><input type="reset" value="リセット" tabindex="10"></td></tr>
</table>
</form>
<br>
<table border="1">
EOF
foreach $line (@allbody) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$line);

print <<"EOF";

<tr>
<td>$ID</td>
<td>$TITLE</td>
<td>$UY</td>
<td>$UM</td>
<td>$UD</td>
<td>$EY</td>
<td>$EM</td>
<td>$ED</td>
<td>$COM</td>
<td>$DATE</td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="DELID" value="$ID"><input type="hidden" name="mode" value="scheduledel"><input type="submit" value="削除"></form></td>
<td><form action="./admin.cgi" method="POST"><input type="hidden" name="REID" value="$ID"><input type="hidden" name="mode" value="schedulere"><input type="submit" value="変更"></form></td>
</tr>

EOF
}

print <<"EOF";
</table></td>
            <td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td height="15"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
            <td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
          </tr>
        </table></td>
    </tr>
  </table>
</div>
</body>
</html>


EOF

}


sub scheduleadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }
if ($DATE eq '') { &error; }

@add = ($UY,$UM,$UD);
$IDADD = join("",@add);

$COM =~ s/\n/<br>/g;

open(FILE,">>$fileschedule");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE\n";
close(FILE);

open(FILE,"<$fileschedule");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$fileschedule");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~ s/ //g;
 $sortadd =~ s///g;
 $sortadd =~ s/\\r\n//g; $sortadd =~ s/\\n//g; $sortadd =~ s/\\r//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$fileschedule");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }

}

open(FILE,">$fileschedule");
print FILE @allbody;;
close(FILE);


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
登録しました。<br>
<input type="button" value="戻る" onclick="history.back()">

</body>
</html>

EOF

}
exit;




sub scheduledel {

open(FILE,"<$fileschedule");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody){
 if ($line =~ /$DELID/){
$line =~ s/.*\n//;
}
 }
open(FILE,">$fileschedule");
print FILE @allbody;
close(FILE);

print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
削除しました。<br>
<input type="button" value="戻る" onclick="history.back()">

</body>
</html>

EOF

}


sub schedulere {

open(FILE,$fileschedule);
@allbody = <FILE>;
close(FILE);

foreach $num (0 .. $#allbody) {

	$line = $line2 = $allbody[$num];
	&jcode'convert(*line,'sjis');
        ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$line);

	# 変更ID(一致)

	if ($REID ne 'all') {

		if ($ID eq $REID) { ; } else { next; }
	}


	# 検索終了処理
	if ($hit == 1) { last; }
	else { push(@NEW,$line2); $hit++; }
}


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff"><div align="center">
  <table border="0" cellpadding="0" cellspacing="0">
    <tr> 
      <td height="34"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190">行事日程</td>
            <td background="../../../images/yakuohji/admin/index_50.gif">&nbsp;</td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_51.gif" WIDTH=15 HEIGHT=34 ALT=""></td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" height="100%" border="0" cellpadding="0" cellspacing="0">
          <tr> 
            <td width="15" background="../../../images/yakuohji/admin/index_20.gif">&nbsp;</td>
            <td align="center" valign="top">
EOF

foreach $line (@NEW) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$line);
$COM =~ s/<br>/\n/g;

print <<"EOF";
<form enctype="multipart/form-data" action="./admin.cgi" method="POST">
<table border="1">
<tr><td>掲載年</td><td><SELECT name="UY" tabindex="1">
 <OPTION value="$UY" selected>$UY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="UM" tabindex="2">
 <OPTION value="$UM" selected>$UM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="UD" tabindex="3">
 <OPTION value="$UD" selected>$UD</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>終了年</td><td><SELECT name="EY" tabindex="1">
 <OPTION value="$EY" selected>$EY</OPTION>
 <OPTION value="2003">2003</OPTION>
 <OPTION value="2004">2004</OPTION>
 <OPTION value="2005">2005</OPTION>
 <OPTION value="2006">2006</OPTION>
 <OPTION value="2007">2007</OPTION>
 <OPTION value="2008">2008</OPTION>
 <OPTION value="2009">2009</OPTION>
 <OPTION value="9999">9999</OPTION>
 </SELECT>年　<SELECT name="EM" tabindex="2">
 <OPTION value="$EM" selected>$EM</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 </SELECT>月　<SELECT name="ED" tabindex="3">
 <OPTION value="$ED" selected>$ED</OPTION>
 <OPTION value="01">01</OPTION>
 <OPTION value="02">02</OPTION>
 <OPTION value="03">03</OPTION>
 <OPTION value="04">04</OPTION>
 <OPTION value="05">05</OPTION>
 <OPTION value="06">06</OPTION>
 <OPTION value="07">07</OPTION>
 <OPTION value="08">08</OPTION>
 <OPTION value="09">09</OPTION>
 <OPTION value="10">10</OPTION>
 <OPTION value="11">11</OPTION>
 <OPTION value="12">12</OPTION>
 <OPTION value="13">13</OPTION>
 <OPTION value="14">14</OPTION>
 <OPTION value="15">15</OPTION>
 <OPTION value="16">16</OPTION>
 <OPTION value="17">17</OPTION>
 <OPTION value="18">18</OPTION>
 <OPTION value="19">19</OPTION>
 <OPTION value="20">20</OPTION>
 <OPTION value="21">21</OPTION>
 <OPTION value="22">22</OPTION>
 <OPTION value="23">23</OPTION>
 <OPTION value="24">24</OPTION>
 <OPTION value="25">25</OPTION>
 <OPTION value="26">26</OPTION>
 <OPTION value="27">27</OPTION>
 <OPTION value="28">28</OPTION>
 <OPTION value="29">29</OPTION>
 <OPTION value="30">30</OPTION>
 <OPTION value="31">31</OPTION>
</SELECT>日
</td></tr>
<tr><td>タイトル</td><td><input type="text" name="TITLE" size="30" tabindex="4" value="$TITLE"></td></tr>
<tr><td>コメント</td><td><TEXTAREA name="COM" rows="5" cols="30" tabindex="7">$COM</TEXTAREA></td></tr>
<tr><td>日付</td><td><input type="text" name="DATE" size="30" tabindex="4" value="$DATE"></td></tr>
<tr><td colspan="2" align="center"><input type="hidden" name="mode" value="schedulereadd"><input type="hidden" name="REID" value="$ID"><input type="submit" value="変更" tabindex="8"></td></tr>
</table>
</form>
EOF
}
print <<"EOF";
<input type="button" value="戻る" onclick="history.back()" tabindex="10">
</td>
            <td width="15" background="../../../images/yakuohji/admin/index_22.gif">&nbsp;</td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td height="15"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190"><IMG SRC="../../../images/yakuohji/admin/index_64.gif" WIDTH=190 HEIGHT=15 ALT=""></td>
            <td background="../../../images/yakuohji/admin/index_65.gif"><font style="1px;line-height:100%">&nbsp;</font></td>
            <td width="15"><IMG SRC="../../../images/yakuohji/admin/index_66.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
          </tr>
        </table></td>
    </tr>
  </table>
</div>
</body>
</html>


EOF

}



sub schedulereadd {

if ($TITLE eq '') { &error; }
if ($UY eq '') { &error; }
if ($UM eq '') { &error; }
if ($UD eq '') { &error; }
if ($EY eq '') { &error; }
if ($EM eq '') { &error; }
if ($ED eq '') { &error; }
if ($COM eq '') { &error; }
if ($DATE eq '') { &error; }

@add = ($UY,$UM,$UD);
$IDADD = join("",@add);

$COM =~ s/\n/\<br\>/g;

open(FILE,"<$fileschedule");
@allbody = <FILE>;
close(FILE);

foreach $line(@allbody){
 if ($line =~ /$REID/){
                    $line =~ s/.*\n//;
                    }
}

open(FILE,">$fileschedule");
print FILE @allbody;
close(FILE);



open(FILE,">>$fileschedule");
print FILE "\n$IDADD,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE\n";
close(FILE);

open(FILE,"<$fileschedule");
@allbody = <FILE>;
@sorted = reverse sort { (split(/\,/,$a))[0] <=> (split(/\,/,$b))[0] } @allbody;
close(FILE);

open(FILE,">$fileschedule");
foreach $line(@sorted) {
 $sortadd = $line;
# $sortadd =~ s/ //g;
 $sortadd =~ s///g;
 $sortadd =~ s/\\r\n//g; $sortadd =~ s/\\n//g; $sortadd =~ s/\\r//g;
 print FILE "\n$sortadd";
 }
close(FILE);

open(FILE,"<$fileschedule");
@allbody = <FILE>;
close(FILE);
foreach $line(@allbody) {
if ($line == "\r\n") { $line =~ s/.*\r\n//; } elsif ($line == "\n") { $line =~ s/.*\n//; } elsif ($line == "\r") { $line =~ s/.*\r//; }

}

open(FILE,">$fileschedule");
print FILE @allbody;;
close(FILE);


print "Content-type: text/html\n\n";
print <<"EOF";

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../../yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="../../../popup.js"></SCRIPT>
</head>
<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
更新しました。<br>
<input type="button" value="戻る" onclick="history.go(-2)">

</body>
</html>

EOF

}


sub error {

	print "Content-type: text/html\n\n";
print "<html><head><title>$title</title></head>\n";
print "$body\n";
print "<h1>$_[0]</h1>\n";
	print "<h3>$_[1]</h3><p>\n";
	print "作業は完了しておりません。<br>ブラウザの[戻る]ボタンを押して前の画面に移動してください.<p>\n";
print "</body></html>\n";
exit;
}
