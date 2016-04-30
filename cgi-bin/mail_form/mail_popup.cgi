#!/usr/bin/perl
#
# 簡易データベース v2.1 (SJIS)　検索用
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

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
#	$value =~ s/\,//g;

	#フォーム変数へ
	$FORM{$name} = $value;
}

$a1 = $FORM{'a1'};
$a2 = $FORM{'a2'};
$a3 = $FORM{'a3'};
$a4 = $FORM{'a4'};
$a5 = $FORM{'a5'};
$a6 = $FORM{'a6'};
$a7 = $FORM{'a7'};
$a8 = $FORM{'a8'};
$a9 = $FORM{'a9'};
$mail = $FORM{'mail'};
$necessary = $FORM{'necessary'};



#■検索結果

print "Content-type: text/html\n\n";
print <<"EOF";

<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=utf-8">
<META http-equiv="Content-Style-Type" content="text/css">
<meta http-equiv="refresh" content="0:url=http://www.hdg.jp/">
<TITLE>七国山薬王寺</TITLE>
<SCRIPT language="JavaScript" src="../../popup.js"></SCRIPT>
</HEAD>
<BODY leftmargin="0" rightmargin="0" topmargin="0" marginwidth="0" marginheight="0" bgcolor="#ffffff" onload="HelpWinOpen('./mail_form.cgi?&a1=$a1&a2=$a2&a3=$a3&a4=$a4&mail=$mail&necessary=$necessary','HELP1',370,300);" onUnload="history.go(-1);">
</body>
</html>

EOF

exit;