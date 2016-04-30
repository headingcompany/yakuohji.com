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
	($ID,$DATE,$COM,$GW,$GH,$NOTE) = split(/\,/,$data);

	# 日付ID(一致)

	if ($FORM{'ID'} ne 'all') {

		if ($ID eq $FORM{'ID'}) { ; } else { next; }
	}


	# 検索終了処理
	if ($hit == $page) { $next_num = $num; last; }
	else { push(@NEW,$data2); $hit++; }
}

#■検索結果

	($ID,$DATE,$COM,$GW,$GH,$NOTE) = split(/\,/,$data);

print "Content-type: text/html\n\n";
print <<"EOF";

<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=utf-8">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE>薬王寺のつつじ / 今日の様子</TITLE>
<STYLE type="text/css">
<!--
TD{
font-size : 12px;
line-height : 150%;
}

A{
text-decoration : none;
color : #ff2200;
}

A:HOVER{
text-decoration : none;
color : #0066ff;
}
-->
</STYLE>
<SCRIPT language="JavaScript">
<!--
var HELPWin=null;//サブウインドウ
var HELPHref1="";//読み込むページ
function HelpWinOpen(HELPHref1,WinNo,W,H){
HELPWin=window.open(HELPHref1,WinNo,'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=0,resizable=0,width='+W+',height='+H+'');
//N2.0バグ回避用リピート
if(navigator.appVersion.charAt(0)==2){
HELPWin=window.open(HELPHref1,WinNo,'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=0,resizable=0,width='+W+',height='+H+'');}
//サブウインドウが開いたとき前面へフォーカスする。NN3.0~
if(navigator.appVersion.charAt(0)>=3){HELPWin.focus()}
};
<!---->
</SCRIPT>

</HEAD>
<BODY leftmargin="0" rightmargin="0" topmargin="0" marginwidth="0" marginheight="0" bgcolor="#ffffff">


EOF


if (!@NEW) {
print <<"EOF";
<center>●ご指定の条件では見当たりませんでした.
</center>
</BODY>
</HTML>
EOF
exit;
}
else {



	foreach $data (@NEW) {

print <<"EOF";

<TABLE border="0" height="100%" cellpadding="0" cellspacing="0">
<TBODY>
<TR>
<TD valign="top">
<TABLE border="0" width="260" cellpadding="3" cellspacing="0">
<TBODY>
<TR>
<TD bgcolor="#ff2200" height="25">
<TABLE border="0" cellpadding="0" cellspacing="0" width="100%">
<TBODY>
<TR>


EOF
	($ID,$DATE,$COM,$GW,$GH,$NOTE) = split(/\,/,$data);


print <<"EOF";


<TD width="50%"><B><FONT color="ffffff" style="font-size:16px;line-height:150%">$DATE</FONT></B></TD>
<TD width="50%" align="right"><IMG src="http://www.t-net.ne.jp/~yakuohji/images/0404tsutsuji_date.gif" width="30" height="18" border="0"></TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
<TR>
<TD align="center"><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='http://www.hdg.jp/cgi-bin/yakuohji/0404tsutsuji/search_popup.cgi?ID=$ID';
WinNo='HELP1';//
W=$GW+6;
H=$GH+56;
HelpWinOpen(HELPHref1,WinNo,W,H)"><IMG src="http://www.t-net.ne.jp/~yakuohji/images/tsutsuji_$ID.jpg" border="0"></a></TD>
</TR>
<TR>
<TD>$COM</TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
<TR>
<TD>

EOF
}



	if ($next_num ne '') {

		while (($key,$val) = each %FORM2) {

			if ($key ne 'FF') { $buf = "$buf&$key=$val"; }
		}

print <<"EOF";

<TABLE border="0" cellpadding="0" cellspacing="0" width="100%">
<TBODY>
<TR>
<TD><a href="javascript:history.back()"><B>≪前ページ</B></a></TD>
<TD align="right"><a href=\"search.cgi?$buf&FF=$next_num\" target="tsutsuji"><B>前日の様子≫</B></A></TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
</TBODY>
</TABLE>
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
<TABLE border="0" cellpadding="0" cellspacing="0" width="100%">
<TBODY>
<TR>
<TD><a href="javascript:history.back()"><B>≪前ページ</B></a></TD>
</TR>
</TBODY>
</TABLE>
</TD>
</TR>
</TBODY>
</TABLE>
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
