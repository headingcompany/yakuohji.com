#!/usr/bin/perl
#
#-----------------------------------------------------------------------------------

#日本語コード処理ライブラリ
require './jcode.pl';

##ファイル設定
#最近の行事
$file = "../text_data/ivent.txt";
$file2 = "../text_data/top.txt";
$file3 = "../text_data/greet.txt";
$file4 = "../text_data/schedule.txt";
$file5 = "../text_data/history.txt";
$file6 = "../text_data/special.txt";

##表示設定
#右側
$P1 = "topnew";
$P2 = "topivent";
$P3 = "topspecial";
$P4 = "";


#-----------------------------------------------------------------------------------

#■入力

if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

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

if ($FORM{'con'} eq '') { $con = "main"; $con_tab = 1; $con_no = 1; $title=""; $bdr=""; $cnm=""; }
   elsif ($FORM{'con'} eq 'main') { $con = "main"; $con_tab = 1; $con_no = 1; $title="トップ"; $bdr=" | "; $cnm=","; }
   elsif ($FORM{'con'} eq 'greet') { $con = "main"; $con_tab = 2; $con_no = 2; $title="ごあいさつ"; $bdr=" | "; $cnm=","; }
   elsif ($FORM{'con'} eq 'his') { $con = "main"; $con_tab = 3; $con_no = 3; $title="歴史"; $bdr=" | "; $cnm=","; }
   elsif ($FORM{'con'} eq 'garden') { $con = "main"; $con_tab = 4; $con_no = 41; $title="境内の紹介 弘法大師"; $bdr=" | "; $cnm=","; }
     elsif ($FORM{'con'} eq 'garden02') { $con = "main"; $con_tab = 4; $con_no = 42; $title="境内の紹介 四国八十八箇所お砂踏み道"; $bdr=" | "; $cnm=","; }
     elsif ($FORM{'con'} eq 'garden03') { $con = "main"; $con_tab = 4; $con_no = 43; $title="境内の紹介 本堂"; $bdr=" | "; $cnm=","; }
     elsif ($FORM{'con'} eq 'garden04') { $con = "main"; $con_tab = 4; $con_no = 44; $title="境内の紹介 四季の花"; $bdr=" | "; $cnm=","; }
     elsif ($FORM{'con'} eq 'garden06') { $con = "main"; $con_tab = 4; $con_no = 46; $title="境内の紹介 護摩堂・不動堂"; $bdr=" | "; $cnm=","; }
     elsif ($FORM{'con'} eq 'garden07') { $con = "main"; $con_tab = 4; $con_no = 47; $title="境内の紹介 山門"; $bdr=" | "; $cnm=","; }
   elsif ($FORM{'con'} eq 'schedule') { $con = "main"; $con_tab = 5;  $con_no = 5; $title="行事日程"; $bdr=" | "; $cnm=","; }
   elsif ($FORM{'con'} eq 'info') { $con = "main"; $con_tab = 6; $con_no = 6; $title="お問合せ"; $bdr=" | "; $cnm=","; }
   elsif ($FORM{'con'} eq 'link') { $con = "main"; $con_tab = 7; $con_no = 7; $title="リンク集"; $bdr=" | "; $cnm=","; }
   elsif ($FORM{'con'} eq 'special') { $con = "main"; $con_tab = 8; $con_no = 8; $title=""; $bdr=" | "; $cnm=","; }
   else { $con = "main"; $con_tab = 1; $title=""; $bdr=""; $cnm=""; $title="トップ"; $bdr=" | "; $cnm=","; }


if ($FORM{'P1'} eq '') { $P1 = $P1; }
   elsif ($FORM{'P1'} eq 'topnew') { $P1 = "topnew"; }
   elsif ($FORM{'P1'} eq 'topivent') { $P1 = "topivent"; }
   elsif ($FORM{'P1'} eq 'toptsutsuji') { $P1 = "toptsutsuji"; }
   elsif ($FORM{'P1'} eq 'topspecial') { $P1 = "topspecial"; }
   elsif ($FORM{'P1'} eq 'spacer') { $P1 = "spacer"; }
   else { $P1 = "topnew"; }

if ($FORM{'P2'} eq '') { $P2 = $P2; }
   elsif ($FORM{'P2'} eq 'topnew') { $P2 = "topnew"; }
   elsif ($FORM{'P2'} eq 'topivent') { $P2 = "topivent"; }
   elsif ($FORM{'P2'} eq 'toptsutsuji') { $P2 = "toptsutsuji"; }
   elsif ($FORM{'P2'} eq 'topspecial') { $P2 = "topspecial"; }
   elsif ($FORM{'P2'} eq 'spacer') { $P2 = "spacer"; }
   else { $P2 = "topivent"; }

if ($FORM{'P3'} eq '') { $P3 = $P3; }
   elsif ($FORM{'P3'} eq 'topnew') { $P3 = "topnew"; }
   elsif ($FORM{'P3'} eq 'topivent') { $P3 = "topivent"; }
   elsif ($FORM{'P3'} eq 'toptsutsuji') { $P3 = "toptsutsuji"; }
   elsif ($FORM{'P3'} eq 'topspecial') { $P3 = "topspecial"; }
   elsif ($FORM{'P3'} eq 'spacer') { $P3 = "spacer"; }
   else { $P3 = "spacer"; }

if ($FORM{'P4'} eq '') { $P4 = $P4; }
   elsif ($FORM{'P4'} eq 'topnew') { $P4 = "topnew"; }
   elsif ($FORM{'P4'} eq 'topivent') { $P4 = "topivent"; }
   elsif ($FORM{'P4'} eq 'toptsutsuji') { $P4 = "toptsutsuji"; }
   elsif ($FORM{'P4'} eq 'topspecial') { $P4 = "topspecial"; }
   elsif ($FORM{'P4'} eq 'spacer') { $P4 = "spacer"; }
   else { $P4 = "spacer"; }


#■最近の行事・検索処理
if (!open(IN,"$file")) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

$hit = 0;
$next_num = '';
$num = 0;
$pnew = 0;

foreach $num (0 .. $#BASE) {
	$data = $data2 = $BASE[$num];
	&jcode'convert(*data,'sjis');
	($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$data);
        ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
        $mon++;
        $year = $year + 1900;

&symd;

	# 検索終了処理
	push(@NEW,$data2); $pivent = $pnew;
}

#■お知らせ・検索処理
if (!open(IN,"$file2")) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

$hit = 0;
$next_num = '';
$num = 0;
$pnew = 0;

foreach $num (0 .. $#BASE) {
	$data3 = $data4 = $BASE[$num];
	&jcode'convert(*data3,'sjis');
	($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM) = split(/\,/,$data3);
	($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
	$mon++;
	$year = $year + 1900;

&symd;

	# 検索終了処理
	push(@NEW2,$data4);  $ptop = $pnew;
}

#■ご挨拶・検索処理
if (!open(IN,"$file3")) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

$hit = 0;
$next_num = '';
$num = 0;
$pnew = 0;
$hit =0;

foreach $num (0 .. $#BASE) {
	$data5 = $data6 = $BASE[$num];
	&jcode'convert(*data5,'sjis');
	($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$data5);
	($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
	$mon++;
	$year = $year + 1900;

&symd;

	# 検索終了処理
	if ($hit eq 0) { push(@NEW3,$data6);  $pgreet = $pnew; $hit++; }
	  else { push(@NEW3_2,$data6); }
}

#■行事日程・検索処理
if (!open(IN,"$file4")) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

$hit = 0;
$next_num = '';
$num = 0;
$pnew = 0;
$hit =0;

foreach $num (0 .. $#BASE) {
	$data7 = $data7_2 = $data8 = $BASE[$num];
	&jcode'convert(*data7,'sjis');
	($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$data7);
	($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
	$mon++;
	$year = $year + 1900;

	&symd;

	# 検索終了処理
	if ($year eq $UY) {
	  if ($hit eq 0) { push(@NEW4,$data8);  $pschedule = $pnew; $hit++; }
	    else { push(@NEW4,$data8); }
        }
	else { push(@NEW4_2,$data8); }
}

#■歴史・検索処理
if (!open(IN,"$file5")) { &error('データベース読取エラー','復旧をお待ちください.'); }
@BASE = <IN>;
close(IN);

$hit = 0;
$next_num = '';
$num = 0;
$pnew = 0;
$hit =0;

foreach $num (0 .. $#BASE) {
	$data9 = $data10 = $BASE[$num];
	&jcode'convert(*data9,'sjis');
	($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$NO,$COM,$COM2,$ST,$URL,$NTITLE) = split(/\,/,$data9);
	($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
	$mon++;
	$year = $year + 1900;

	&symd;

	# 検索終了処理
	if ($hit eq 0) { push(@NEW5,$data10);  $phistory = $pnew; $hit++; }
	else { push(@NEW5_2,$data10); }
}


#■特設ページ・検索処理
if (!open(IN,"$file6")) { &error('データベース読取エラー','復旧をお待ちください1.'); }
@BASE = <IN>;
close(IN);

$hit = 0;
$next_num = '';
$num = 0;
$pnew = 0;
$hit = 0;

foreach $num (0 .. $#BASE) {
	$data11 = $data11_2 = $data12 = $BASE[$num];
	&jcode'convert(*data11,'sjis');
	($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$MY,$MM,$MD,$IV,$URL) = split(/\,/,$data11);
	($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
	$mon++;
	$year = $year + 1900;

	&symd;

	push(@NEW6_3,$data12);

	# 検索終了処理
	if ($hit eq 0) {
		if ($FORM{'ID'} eq $ID && $FORM{'con'} eq 'special') {
			push(@NEW6,$data12);
			$pspecial = $pnew;
			$hit++;

			if ($IV eq "1") {
				@add = ("../text_data/special_tsutsuji_",$ID,".txt");
				$file7 = join("",@add);

				if (!open(IN,"$file7")) { &error('データベース読取エラー','復旧をお待ちください2.'); }
				@BASEdata = <IN>;
				close(IN);

				$page = 1;

				if ($FORM{'FF'} eq '') { $FF = 0; } else { $FF = $FORM{'FF'}; }
				$TO = $FF + $page - 1;
				if ($TO > $#BASEdata) { $TO = $#BASEdata; }

				$hitdata = 0;
				$next_numdata = '';
				$numdata = 0;
				$pnewdata = 0;
				$hitdata = 0;

				foreach $num ($FF .. $#BASEdata) {
					$data13 = $data14 = $BASEdata[$num];
					&jcode'convert(*data13,'sjis');
					($ID_T,$TITLE_T,$UY_T,$UM_T,$UD_T,$COM_T) = split(/\,/,$data13);

					# 検索終了処理
					if ($hitdata eq $page) {
						$next_numdata = $num;
						last;
					}
					else {
						$spTit = " ". $TITLE ." ". $UM_T ."月".$UD_T."日";
						$hitdata++;
					}
				}
			} else {
				$spTit = " ". $TITLE;
			}
			next;
		} elsif ($FORM{'ID'} eq "" && $FORM{'con'} eq 'special') {
			push(@NEW6,$data12);
			$pspecial = $pnew;
			$hit++;

			if ($IV eq "1") {
				@add = ("../text_data/special_tsutsuji_",$ID,".txt");
				$file7 = join("",@add);

				if (!open(IN,"$file7")) { &error('データベース読取エラー','復旧をお待ちください2.'); }
				@BASEdata = <IN>;
				close(IN);

				$page = 1;

				if ($FORM{'FF'} eq '') { $FF = 0; } else { $FF = $FORM{'FF'}; }
				$TO = $FF + $page - 1;
				if ($TO > $#BASEdata) { $TO = $#BASEdata; }

				$hitdata = 0;
				$next_numdata = '';
				$numdata = 0;
				$pnewdata = 0;
				$hitdata = 0;

				foreach $num ($FF .. $#BASEdata) {
					$data13 = $data14 = $BASEdata[$num];
					&jcode'convert(*data13,'sjis');
					($ID_T,$TITLE_T,$UY_T,$UM_T,$UD_T,$COM_T) = split(/\,/,$data13);

					# 検索終了処理
					if ($hitdata eq $page) {
						$next_numdata = $num;
						last;
					}
					else {
						$spTit = " ". $TITLE ." ". $UM_T ."月".$UD_T."日";
						$hitdata++;
					}
				}
			} else {
				$spTit = " ". $TITLE;
			}
			next;
		}
		else {
			push(@NEW6_2,$data12);
			next;
		}
	}
	push(@NEW6_2,$data12);

}


#■特設ページ_つつじ表示部分・検索処理
sub serch_special_tstsuji {
  if (!open(IN,"$file7")) { &error('データベース読取エラー','復旧をお待ちください.'); }
  @BASE = <IN>;
  close(IN);

$page = 1;

if ($FORM{'FF'} eq '') { $FF = 0; } else { $FF = $FORM{'FF'}; }
$TO = $FF + $page - 1;
if ($TO > $#BASE) { $TO = $#BASE; }

  $hit = 0;
  $next_num = '';
  $num = 0;
  $pnew = 0;
  $hit = 0;

  foreach $num ($FF .. $#BASE) {
	$data13 = $data14 = $BASE[$num];
	&jcode'convert(*data13,'sjis');
	($ID_T,$TITLE_T,$UY_T,$UM_T,$UD_T,$COM_T) = split(/\,/,$data13);

	# 検索終了処理
#	if ($ID_T eq $FORM{'ID_T'}) {
	  if ($hit eq $page) { $next_num = $num; last;}
	    else { push(@NEW7,$data14); $hit++; }
#	}
  }
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


sub msymd {
  if ($UY <= $year) {
    if ($UM <= $mon) {
      if ($UD <= $day) { &mendymd2; }
      else {
        if ($UM < $mon) { &mendymd2; }
        else { next; }
      }
    }
    else{
      if ($UY < $year) { &mendymd2; }
      else { next; }
    }
  }
  else{ next; }
}

sub mendymd {
  if ($MY >= $year) {
    if ($MM >= $mon) {
      if ($MD >= $day) { ; }
      else {
        if ($MM > $mon) { ; }
        else {
          if ($MY > $year) { ; }
          else { $pend = 1; }
        }
      }
    }
    else{
      if ($MY > $year) { ; }
      else { $pend = 1; }
    }
  }
  else{ $pend = 1; }

}


#■検索結果

print "Content-type: text/html\n\n";
print <<"EOF";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
EOF
print '<title>' . $title . $spTit . $bdr . '七国山薬王寺 | 真言宗豊山派 東京都青梅市にあるつつじのお寺</title>
<meta name="description" content="'. $title . $spTit . $bdr . '東京都青梅市にある、真言宗豊山派のお寺・七国山薬王寺です。つつじの開花状況は毎日更新します。">
<meta name="keywords" content="'. $title . $cnm .'真言宗,豊山,派,祈願,護摩,水子供養,先祖供養,つつじ,開花">';
print <<"EOF";
<link href="/common/css/top.css" rel="stylesheet" type="text/css" />
<link href="/common/css/common.css" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="/common/css/yakuohji_text.css" type="text/css">
<SCRIPT language="JavaScript" src="/common/js/popup.js"></SCRIPT>
<SCRIPT language="JavaScript" src="/common/js/rollover.js"></SCRIPT>
</head>

<!-- moved:2008/11/03 -->
<body bgcolor="#ff6600" leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3">
<table width="950" border="0" cellspacing="0" cellpadding="0" class="autoM">
<tr>
<td valign="top">
<table border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td><h1><a href="/index.html" target="_self" class="title ti bDisp" title="$title$spTit$bdr七国山薬王寺 | 真言宗豊山派 東京都青梅市にあるつつじのお寺">$title$spTit$bdr七国山薬王寺 | 真言宗豊山派 東京都青梅市にあるつつじのお寺</a></h1></td>
    <td width="10">　</td>
  </tr>
</table>
</td>
<td width="465" valign="top"> 
EOF

if ($con eq "main") { &con_main; }

print <<"EOF";
</td>
<td width="10">&nbsp;</td>
<td width="200" valign="top">
<table width="200" border="0" cellspacing="0" cellpadding="0">
  <tr> 
    <td height="15"><font style="font-size:1px;line-height:100%">&nbsp;</font></td>
  </tr>
  <tr>
    <td>
	  <table width="100%" border="0" cellspacing="0" cellpadding="0">
EOF

if ($P1 eq "topnew") { &topnew; }
   elsif ($P1 eq "topivent") { &topivent; }
   elsif ($P1 eq "toptsutsuji") { &toptsutsuji; }
   elsif ($P1 eq "topspecial") { &topspecial; }
   elsif ($P1 eq "spacer") { &spacer; }

&spacer;

if ($P2 eq "topnew") { &topnew; }
   elsif ($P2 eq "topivent") { &topivent; }
   elsif ($P2 eq "toptsutsuji") { &toptsutsuji; }
   elsif ($P2 eq "topspecial") { &topspecial; }
   elsif ($P2 eq "spacer") { &spacer; }

&spacer;

if ($P3 eq "topnew") { &topnew; }
   elsif ($P3 eq "topivent") { &topivent; }
   elsif ($P3 eq "toptsutsuji") { &toptsutsuji; }
   elsif ($P3 eq "topspecial") { &topspecial; }
   elsif ($P3 eq "spacer") { &spacer; }

&spacer;

if ($P4 eq "topnew") { &topnew; }
   elsif ($P4 eq "topivent") { &topivent; }
   elsif ($P4 eq "toptsutsuji") { &toptsutsuji; }
   elsif ($P4 eq "topspecial") { &topspecial; }
   elsif ($P4 eq "spacer") { &spacer; }

print <<"EOF";
</table>
</td>
</tr>
<tr>
<td>
</td>
</tr>
</table>
</td>
</tr>
</table>
<table width="950" border="0" cellspacing="0" cellpadding="0" class="autoM">
<tr> 
<td align="center">
<br>
<hr width="950" size="1" color="#ffffff">
</td>
</tr>
<tr>
<td align="right"><FONT color="ffffff">copyright 2000-2009 yakuohji.</FONT></td>
</tr>
<tr> 
<td align="left"></td>
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

exit;

##メインコンテンツ##############################################################
#新着情報セクション
sub topnew {
print <<"EOF";
        <tr>
          <td align="right" valign="top">
      <table width="200" border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="110"><IMG SRC="../../images/new_01.gif" WIDTH=110 HEIGHT=15 ALT=""></td>
                <td background="../../images/new_02.gif" style="font-size:1px;line-height:1%;">&nbsp;</td>
                <td width="60"><IMG SRC="../../images/new_03.gif" WIDTH=60 HEIGHT=15 ALT=""></td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="10" background="../../images/new_04.gif">&nbsp;</td>
                <td class="bgWhite">
                  <table width="100%" border="0" cellspacing="3" cellpadding="0">
EOF
if ($pivent eq "1") {
  $hit = 0;
  foreach $data (@NEW) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$data);
    ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    $mon++;
    $year = $year + 1900;

    @add = ($UY,$UM,$UD); $cddate = join("",@add);

    if ($mon < 10) { $inzero_m = "0"; } else { $inzero_m = ""; }
    if ($day < 10) { $inzero_d = "0"; } else { $inzero_d = ""; }
    @add2 = ($year,$inzero_m,$mon,$inzero_d,$day); $ctdate = join("",@add2);

    $cddate = $ctdate - $cddate;

    if ($hit eq 0) {
      if ($cddate < 7)  {
print <<"EOF";
                    <tr>
                      <td valign="top" width="10">・</td>
                      <td>『<A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/event_$ID.html?ST=$ST&URL=$URL';
WinNo='HELP2';//
W=475;
H=510;
HelpWinOpen(HELPHref1,WinNo,W,H)">最近の行事</a>』が掲載されました（$UY/$UM/$UD）</td>
                    </tr>
EOF
      }
      else { $civ = 1; }
    }
    $hit++;
  }
}

if ($ptop eq "1") {
  $hit = 0;
  foreach $data3 (@NEW2) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM) = split(/\,/,$data3);
    ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    $mon++;
    $year = $year + 1900;

    @add = ($UY,$UM,$UD); $cddate = join("",@add);
    if ($mon < 10) { $inzero_m = "0"; } else { $inzero_m = ""; }
    if ($day < 10) { $inzero_d = "0"; } else { $inzero_d = ""; }
    @add2 = ($year,$inzero_m,$mon,$inzero_d,$day); $ctdate = join("",@add2);
    $cddate = $ctdate - $cddate;

    if ($hit eq 0) {
      if ($cddate < 7) {
print <<"EOF";
                    <tr>
                      <td valign="top" width="10">・</td>
                      <td>『<a href="/index.html" target="_self">お知らせ</a>』が掲載されました（$UY/$UM/$UD）</td>
                    </tr>
EOF
      }
      else { $cnew = 1; }
    }
    $hit++;
  }
}

if ($pgreet eq "1") {
  $hit = 0;
  foreach $data5 (@NEW3) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM) = split(/\,/,$data5);
    ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    $mon++;
    $year = $year + 1900;

    @add = ($UY,$UM,$UD); $cddate = join("",@add);
    if ($mon < 10) { $inzero_m = "0"; } else { $inzero_m = ""; }
    if ($day < 10) { $inzero_d = "0"; } else { $inzero_d = ""; }
    @add2 = ($year,$inzero_m,$mon,$inzero_d,$day); $ctdate = join("",@add2);
    $cddate = $ctdate - $cddate;

    if ($hit eq 0) {
      if ($cddate < 7) {
print <<"EOF";
                    <tr>
                      <td valign="top" width="10">・</td>
                      <td>『<a href="/greet.html" target="_self">ご挨拶</a>』が掲載されました（$UY/$UM/$UD）</td>
                    </tr>
EOF
      }
      else { $cgreet = 1; }
    }
    $hit++;
  }
}


if ($pschedule eq "1") {
  $hit = 0;
  foreach $data7 (@NEW4) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$data7);
    ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    $mon++;
    $year = $year + 1900;

    @add = ($UY,$UM,$UD); $cddate = join("",@add);
    if ($mon < 10) { $inzero_m = "0"; } else { $inzero_m = ""; }
    if ($day < 10) { $inzero_d = "0"; } else { $inzero_d = ""; }
    @add2 = ($year,$inzero_m,$mon,$inzero_d,$day); $ctdate = join("",@add2);
    $cddate = $ctdate - $cddate;

#    $UM++;
#    if ($UM eq "13") { $UM = 11; }

    if ($hit eq 0) {
      if ($cddate < 7) {
print <<"EOF";
                    <tr>
                      <td valign="top" width="10">・</td>
                      <td>『<a href="/schedule.html" target="_self">行事日程</a>』が掲載されました（$UY/$UM/$UD）</td>
                    </tr>
EOF
      }
      else { $cschedule = 1; }
    }
    $hit++;
  }
}


if ($phistory eq "1") {
  $hit = 0;
  foreach $data9 (@NEW5) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$NO,$COM,$COM2,$ST,$URL,$NTITLE) = split(/\,/,$data9);
    ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    $mon++;
    $year = $year + 1900;

    @add = ($UY,$UM,$UD); $cddate = join("",@add);
    if ($mon < 10) { $inzero_m = "0"; } else { $inzero_m = ""; }
    if ($day < 10) { $inzero_d = "0"; } else { $inzero_d = ""; }
    @add2 = ($year,$inzero_m,$mon,$inzero_d,$day); $ctdate = join("",@add2);

    $cddate = $ctdate - $cddate;

    if ($hit eq 0) {
      if ($cddate < 7) {
print <<"EOF";
                    <tr>
                      <td valign="top" width="10">・</td>
                      <td>『<a href="/his.html" target="_self">歴史</a>』が掲載されました（$UY/$UM/$UD）</td>
                    </tr>
EOF
      }
      else { $chistory = 1; }
    }
    $hit++;
  }
}



if ($pspecial eq "1") {
  $hit = 0;
  foreach $data11 (@NEW6) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$MY,$MM,$MD,$IV,$URL) = split(/\,/,$data11);
    ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    $mon++;
    $year = $year + 1900;

    @add = ($UY,$UM,$UD); $cddate = join("",@add);
    if ($mon < 10) { $inzero_m = "0"; } else { $inzero_m = ""; }
    if ($day < 10) { $inzero_d = "0"; } else { $inzero_d = ""; }
    @add2 = ($year,$inzero_m,$mon,$inzero_d,$day); $ctdate = join("",@add2);
    $cddate = $ctdate - $cddate;

    if ($hit eq 0) {
      if ($cddate < 7) {
print <<"EOF";
                    <tr>
                      <td valign="top" width="10">・</td>
                      <td>『<a href="/special.html&ID=$ID" target="_self">特設ページ</a>』が掲載されました（$UY/$UM/$UD）</td>
                    </tr>
EOF
      }
      else { $cspecial = 1; }
    }
    $hit++;
  }
}

if ($civ eq "1") {
  if ($cnew eq "1") {
    if ($cgreet eq "1") {
      if ($cschedule eq "1") {
        if ($cspecial eq "1") {
          if ($chistory eq "1") {
            if ($cspecial eq "1") {
print <<"EOF";
                    <tr>
                      <td valign="top" width="10">・</td>
                      <td>最近の更新情報はありません。</td>
                    </tr>
EOF
            }
          }
        }
      }
    }
  }
}
print <<"EOF";
                  </table>
                </td>
                <td width="10" background="../../images/new_06.gif">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr> 
          <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="110"><IMG SRC="../../images/new_07.gif" WIDTH=110 HEIGHT=10 ALT=""></td>
                <td background="../../images/new_08.gif"><font style="font-size:1px;line-height:100%">&nbsp;</font></td>
                <td width="60"><IMG SRC="../../images/new_09.gif" WIDTH=60 HEIGHT=10 ALT=""></td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
          </td>
        </tr>
EOF
}
#新着情報セクション・ここまで
################################################################################
#最近の行事セクション
sub topivent {
$hit = 0;
    foreach $data (@NEW) {
  if ($hit eq 0) {
      ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$ST,$URL,$GRPHNO,$COM2,$COM3) = split(/\,/,$data);
      $COM2 = "";
      ($COM3,$COM4) = split(/\<br>/,$COM);
      $COM2 = substr($COM3,0,50);

      @add = ("../../images/ivent/",$ID,"s.jpg"); $grph01 = join("",@add);

print <<"EOF";
<tr>
  <td align="right">
    <table width="200" border="0" cellpadding="0" cellspacing="0">
      <tr>
        <td>
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td width="110"><IMG SRC="../../images/ivent_01.gif" WIDTH=110 HEIGHT=15 ALT=""></td>
              <td background="../../images/new_02.gif" style="font-size:1px;line-height:1%;">&nbsp;</td>
              <td width="60"><IMG SRC="../../images/ivent_03.gif" WIDTH=60 HEIGHT=15 ALT=""></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td>
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td width="10" background="../../images/new_04.gif">&nbsp;</td>
              <td class="bgWhite">
                <table width="100%" border="0" cellspacing="0" cellpadding="3">
EOF
if ($GRPHNO eq "0") { ; }
else {
print <<"EOF";
                  <tr>
                    <td align="center">
                      <br>
                      <table border="0" cellpadding="0" cellspacing="1" bgcolor="#000000">
                        <tr>
                          <td class="bgWhite"><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/event_$ID.html';
WinNo='HELP2';//
W=475;
H=510;
HelpWinOpen(HELPHref1,WinNo,W,H)"><IMG SRC="$grph01" border="0"></a></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
EOF
}
print <<"EOF";
                  <tr>
                    <td>
                      <hr size="1">
                      <table width="100%" border="0" cellspacing="0" cellpadding="2">
                        <tr>
                          <td valign="top"><strong>$UY/$UM/$UD：</strong></td>
                          <td><strong><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/event_$ID.html';
WinNo='HELP2';//
W=475;
H=510;
HelpWinOpen(HELPHref1,WinNo,W,H)">$TITLE</a></strong></td>
                        </tr>
                      </table>
                      <hr width="90%" size="1">
                      $COM2...
                    </td>
                  </tr>
                  <tr>
                    <td align="right"><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/event_$ID.html';
WinNo='HELP2';//
W=475;
H=510;
HelpWinOpen(HELPHref1,WinNo,W,H)">続きはこちら≫</a></td>
                  </tr>
                </table>
              </td>
              <td width="10" background="../../images/new_06.gif">&nbsp;</td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td>
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td width="110"><IMG SRC="../../images/new_07.gif" WIDTH=110 HEIGHT=10 ALT=""></td>
              <td background="../../images/new_08.gif"><font style="font-size:1px;line-height:100%">&nbsp;</font></td>
              <td width="60"><IMG SRC="../../images/new_09.gif" WIDTH=60 HEIGHT=10 ALT=""></td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </td>
</tr>
EOF
    $hit++;
    }
  }
}
#最近の行事セクション・ここまで
################################################################################
#特設ページセクション
sub topspecial {
print <<"EOF";
<tr>
<td>
<table width="200" border="0" cellpadding="0" cellspacing="0">
<tr> 
<td><table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td width="110"><IMG SRC="../../images/images/special_01.gif" WIDTH=110 HEIGHT=15 ALT=""></td>
<td background="../../images/new_02.gif" style="font-size:1px;line-height:1%;">&nbsp;</td>
<td width="70"><img src="../../images/images/special_03.gif" width=70 height=15 alt=""></td>
</tr>
</table></td>
</tr>
<tr> 
<td>
<table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td width="10" background="../../images/new_04.gif">&nbsp;</td>
<td class="bgWhite"><table width="100%" border="0" cellspacing="3" cellpadding="0">
EOF
  foreach $data11 (@NEW6_3) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$MY,$MM,$MD,$IV,$URL) = split(/\,/,$data11);
print <<"EOF";
<tr> 
<td width="10" valign="top">・</td>
<td><a href="/special.html&ID=$ID" target="_self">$TITLE</a>が掲載されています（$UY/$UM/$UD～$MY/$MM/$MD）</td>
</tr>
EOF
  }
print <<"EOF";
</table></td>
<td width="10" background="../../images/new_06.gif">&nbsp;</td>
</tr>
</table></td>
</tr>
<tr> 
<td> <table width="100%" border="0" cellspacing="0" cellpadding="0">
<tr> 
<td width="110"><IMG SRC="../../images/new_07.gif" WIDTH=110 HEIGHT=10 ALT=""></td>
<td background="../../images/new_08.gif"><font style="font-size:1px;line-height:100%">&nbsp;</font></td>
<td width="60"><IMG SRC="../../images/new_09.gif" WIDTH=60 HEIGHT=10 ALT=""></td>
</tr>
</table></td>
</tr>
</table>
  </td>
</tr>
EOF
}
#特設ページセクション・ここまで
################################################################################
#スペーサーセクション
sub spacer {
print <<"EOF";
<!--スペーサー-->
  <tr>
    <td>&nbsp;</td>
  </tr>
<!--スペーサー-->
EOF
}
#スペーサーセクション・ここまで
################################################################################
#メインコンテンツセクション
sub con_main {
print <<"EOF";
  <table width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
      <td>&nbsp;</td>
    </tr>
    <tr>
      <td>
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td>
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
              	<tr>
              		<td>
              			<ul class="menu1 nonMp nonMark">
EOF
if ($con_tab eq "1") {
print <<"EOF";
<li class="flL nonMp"><h2><img src="../../images/tab/tab_information_local.gif" alt="トップ" name="Image9" width="100" height="25" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li class="flL nonMp"><a href="/index.html" target="_self" class="menu1_info bDisp ti" title="トップ">トップ</a></li>
EOF
}


if ($con_tab eq "2") {
print <<"EOF";
<li class="flL nonMp"><h2><img src="../../images/tab/tab_greeting_local.gif" alt="ごあいさつ" name="Image3" width="100" height="25" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li class="flL nonMp"><a href="/greet.html" target="_self" class="menu2_greet bDisp ti" title="ごあいさつ">ごあいさつ</a></li>
EOF
}

if ($con_tab eq "3") {
print <<"EOF";
<li class="flL nonMp"><h2><img src="../../images/tab/tab_history_local.gif" alt="歴史" name="Image4" width="100" height="25" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li class="flL nonMp"><a href="/his.html" target="_self" class="menu3_history bDisp ti" title="歴史">歴史</a></li>
EOF
}
print <<"EOF";
						</ul>
					</td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td>
              <table width="100%" height="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td valign="top" class="bgWhite">
                    <table width="100%" height="100%" border="0" cellspacing="3" cellpadding="3">
                      <tr>
                        <td valign="top" class="bgWhite">
EOF

  if ($con_no eq "1") { &main_top; }
  elsif ($con_no eq "2") { &main_greet; }
  elsif ($con_no eq "3") { &main_history; }
  elsif ($con_tab eq "4") { &main_garden; }
  elsif ($con_no eq "5") { &main_schedule; }
  elsif ($con_no eq "6") { &main_info; }
  elsif ($con_no eq "7") { &main_link; }
  elsif ($con_no eq "8") { &main_special; }
    else { &main_top; }
print <<"EOF";
                        </td>
                      </tr>
                    </table>
                  </td>
                  <td valign="top" width="25"> 
                    <table width="25" border="0" cellspacing="0" cellpadding="0">
                      <tr>
                      	<td>
							<ul class="menu2 nonMark nonMp">
EOF
if ($con_tab eq "4") {
print <<"EOF";
<li class="nonMp"><h2><img src="../../images/tab/tab_garden_local.gif" alt="境内の紹介 弘法大師" name="Image5" width="25" height="100" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li class="nonMp"><a href="/garden.html" target="_self" class="menu4_garden bDisp ti" title="境内の紹介">境内の紹介</a></li>
EOF
}
if ($con_tab eq "5") {
print <<"EOF";
<li class="nonMp"><h2><img src="../../images/tab/tab_ivent_local.gif" alt="行事日程" name="Image6" width="25" height="100" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li class="nonMp"><a href="/schedule.html" target="_self" class="menu5_event bDisp ti" title="行事日程">行事日程</a></li>
EOF
}
if ($con_tab eq "6") {
print <<"EOF";
<li class="nonMp"><h2><img src="../../images/tab/tab_contact_local.gif" alt="お問合せ" name="Image7" width="25" height="100" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li><a href="/info.php" target="_self" class="menu6_contact bDisp ti" title="お問合せ">お問合せ</a></li>
EOF
}
if ($con_tab eq "7") {
print <<"EOF";
<li class="nonMp"><h2><img src="../../images/tab/tab_link_local.gif" alt="リンク集" name="Image8" width="25" height="100" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li class="nonMp"><a href="/link.html" target="_self" class="menu7_link bDisp ti" title="リンク集">リンク集</a></li>
EOF
}
if ($con_tab eq "8") {
print <<"EOF";
<li class="nonMp"><h2><img src="../../images/tab/tab_special_local.gif" alt="特設ページ" name="Image10" width="25" height="100" border="0"></h2></li>
EOF
}
else {
print <<"EOF";
<li class="nonMp"><a href="/special.html" target="_self" class="menu8_special bDisp ti" title="特設ページ">特設ページ</a></li>
EOF
}
print <<"EOF";
						</td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
EOF
}
#メインコンテンツセクション・ここまで
################################################################################
#メインコンテンツ・お知らせセクション
sub main_top {
print <<"EOF";
<TABLE width="430" cellpadding="3" cellspacing="3" bgcolor="#ff6600">
	<TR> 
		<TD>
			<div id="fb-root"></div><script>(function(d, s, id) {  var js, fjs = d.getElementsByTagName(s)[0];  if (d.getElementById(id)) return;  js = d.createElement(s); js.id = id;  js.src = "//connect.facebook.net/ja_JP/sdk.js#xfbml=1&version=v2.3";  fjs.parentNode.insertBefore(js, fjs);}(document, 'script', 'facebook-jssdk'));</script><div class="fb-video" data-allowfullscreen="true" data-href="https://www.facebook.com/yakuohji/videos/903223793061260/"><div class="fb-xfbml-parse-ignore"><blockquote cite="/yakuohji/videos/903223793061260/"><a href="/yakuohji/videos/903223793061260/"></a><p>バーチャル参拝、的な…</p>Posted by <a href="https://www.facebook.com/yakuohji">真言宗 豊山派 七国山 薬王寺</a> on 2015年4月27日</blockquote></div></div>
		</TD>
	</TR>
EOF
foreach $data3 (@NEW2) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM) = split(/\,/,$data3);
print <<"EOF";
  <TR> 
    <TD><B><FONT color="#ffffff" style="font-size:12px">$UY/$UM/$UD</FONT></B></TD>
  </TR>
  <TR> 
    <TD class="bgWhite">$COM</TD>
  </TR>
EOF
}
print <<"EOF";
</TABLE>
EOF
}
#メインコンテンツ・お知らせセクション・ここまで
################################################################################
#メインコンテンツ・ごあいさつセクション
sub main_greet {
$hit = 0;
foreach $data5 (@NEW3) {
  if ($hit eq 0) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$data5);
    @addupdate = ($UY,$UM,$UD); $update = join("",@addupdate);
    @add = ("../../images/greeting_",$GEN,"_01.jpg"); $grph01 = join("",@add);
    @add2 = ("../../images/greeting_",$GEN,"_",$update,"_02.jpg"); $grph02 = join("",@add2);
    @add3 = ("../../images/greeting_",$GEN,"_03.jpg"); $grph03 = join("",@add3);
    @add4 = ("../../images/greeting_",$GEN,"_04.gif"); $grph04 = join("",@add4);
print <<"EOF";
<table width="300" border="0" cellpadding="0" cellspacing="0" class="autoM bgWhite">
  <tr>
    <td height="5"><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
  </tr>
  <tr> 
    <td align="right"><IMG src="$grph01" width="300" height="244" border="0"></td>
  </tr>
  <tr> 
    <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr> 
          <td valign="top"> <table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr> 
                <td align="right"><img src="$grph02" width="229" height="42"></td>
              </tr>
              <tr> 
                <td>
                 <table border="0" cellspacing="0" cellpadding="0">
                    <tr> 
                      <td width="5">&nbsp;</td>
                      <td>$COM</td>
                    </tr>
                  </table></td>
              </tr>
              <tr>
                <td align="right">（$UY/$UM/$UD掲載）</td>
              <tr> 
                <td align="center"><br>
                  <table border="0" cellspacing="0" cellpadding="3">
                    <tr> 
                      <td><IMG src="../../images/imagemark.gif" alt="和違い" width="20" height="20" border="0"></td>
                      <td><strong><font color="#ff2200">次回は「$NTITLE」をお送りします。</font></strong></td>
                    </tr>
                  </table> <hr size="1">
                  <table border="0" cellpadding="0" cellspacing="0" bgcolor="#ff6600">
                    <tr> 
                      <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_01.gif" width="5" height="5" border="0"></td>
                      <td><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
                      <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_02.gif" width="5" height="5" border="0"></td>
                    </tr>
                    <tr> 
                      <td><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
                      <td>
                        <table border="0" cellspacing="1" cellpadding="3">
EOF
foreach $data5 (@NEW3_2) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$GEN,$NTITLE) = split(/\,/,$data5);
    @addupdate = ($UY,$UM,$UD); $update = join("",@addupdate);
print <<"EOF";
                          <tr class="bgWhite">
                            <td valign="top"><strong>$UY/$UM/$UD</strong></td>
                            <td><strong><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/greet_$ID.html';
WinNo='HELP1';//
W=350;
H=500;
HelpWinOpen(HELPHref1,WinNo,W,H)">$TITLE</a></strong></td>
                          </tr>
EOF
}
print <<"EOF";
                        </table></td>
                      <td><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
                    </tr>
                    <tr> 
                      <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_03.gif" width="5" height="5" border="0"></td>
                      <td><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
                      <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_04.gif" width="5" height="5" border="0"></td>
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
</table>
EOF
$hit++;
    }
  }
}
#メインコンテンツ・ごあいさつセクション・ここまで
################################################################################
#メインコンテンツ・歴史セクション
sub main_history {
$hit = 0;
foreach $data9 (@NEW5) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$NO,$COM,$COM2,$ST,$URL,$NTITLE) = split(/\,/,$data9);
print <<"EOF";
<table width="430" border="0" cellspacing="0" cellpadding="0">
  <tr> 
    <td>
EOF
if ($ST eq "1") { &main_his_url; }
 else { ; }
print <<"EOF";
    </td>
  </tr>
  <tr>
    <td height="10"><font style="font-size:1px;line-height:1%">&nbsp;</font></td>
  </tr>
  <tr>
    <td>
      <table border="0" cellspacing="0" cellpadding="3">
        <tr> 
          <td><IMG src="../../images/imagemark.gif" width="20" height="20" border="0"></td>
          <td><B><FONT color="ff2200">次回は「$NTITLE」をお送りします。</FONT></B></td>
        </tr>
      </table></td>
  </tr>
  <tr> 
    <td align="center"><hr border="1"><table border="0" cellpadding="0" cellspacing="0" bgcolor="#ff6600">
        <tr> 
          <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_01.gif" width="5" height="5" border="0"></td>
          <td><font style="font-size:1pz;line-height:1%">&nbsp;</font></td>
          <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_02.gif" width="5" height="5" border="0"></td>
        </tr>
        <tr> 
          <td>&nbsp;</td>
          <td><table width="100%" border="0" cellspacing="1" cellpadding="3">
EOF
foreach $data9 (@NEW5_2) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$NO,$COM,$COM2,$ST,$URL,$NTITLE) = split(/\,/,$data9);
print <<"EOF";
              <tr class="bgWhite"> 
                <td align="center"><strong>$NO</strong></td>
                <td><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/history_$ID.html';
WinNo='HELP6';//
W=350;
H=500;
HelpWinOpen(HELPHref1,WinNo,W,H)">$TITLE</a></td>
              </tr>
EOF
}
print <<"EOF";
            </table></td>
          <td>&nbsp;</td>
        </tr>
        <tr> 
          <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_03.gif" width="5" height="5" border="0"></td>
          <td><font style="font-size:1pz;line-height:1%">&nbsp;</font></td>
          <td width="5" height="5"><IMG src="../../images/history_backup_edge_now_04.gif" width="5" height="5" border="0"></td>
        </tr>
      </table></td>
  </tr>
</table>
EOF
}
}

sub main_his_url {
  open (IN,"$URL");
  while(<IN>){ print; }
  close(IN);
}

#メインコンテンツ・歴史セクション・ここまで
################################################################################
#メインコンテンツ・境内セクション
sub main_garden {

if ($con_no eq "41") {
  open (IN,"../../contents/garden/garden_01kukai.html");
  while(<IN>){ print; }
  close(IN);
}

if ($con_no eq "42") {
  open (IN,"../../contents/garden/garden_02michi.html");
  while(<IN>){ print; }
  close(IN);
}

if ($con_no eq "43") {
  open (IN,"../../contents/garden/garden_03hondo.html");
  while(<IN>){ print; }
  close(IN);
}

if ($con_no eq "44") {
  open (IN,"../../contents/garden/garden_04hana.html");
  while(<IN>){ print; }
  close(IN);
}

if ($con_no eq "46") {
  open (IN,"../../contents/garden/garden_06goma.html");
  while(<IN>){ print; }
  close(IN);
}

if ($con_no eq "47") {
  open (IN,"../../contents/garden/garden_07mon.html");
  while(<IN>){ print; }
  close(IN);
}


}
#メインコンテンツ・境内セクション・ここまで
################################################################################
#メインコンテンツ・行事日程セクション
sub main_schedule {
$hit = 0;
print <<"EOF";
<table width="430" border="0" cellpadding="0" cellspacing="0" bgcolor="#ff6600">
	<tr>
    <td><table width="100%" border="0" cellspacing="3" cellpadding="1">
        <tr bgcolor="#ff9933">
          <td><font color="ffffff"><strong>日付</strong></font></td>
          <td><font color="ffffff"><strong>行事内容</strong></font></td>
        </tr>
EOF
foreach $data7 (@NEW4) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$data7);
print <<"EOF";
        <tr class="bgWhite">
          <td>$DATE</td>
          <td>$COM</td>
        </tr>
EOF
}
print <<"EOF";
      </table></td>
  </tr>
  <tr>
    <td class="bgWhite">
      <table border="0" cellspacing="0" cellpadding="5">
        <tr>
EOF
foreach $data7_2 (@NEW4_2) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$COM,$DATE) = split(/\,/,$data7_2);
if ($UY ne $UY2) {
print <<"EOF";
          <td><strong><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/cgi-bin/schedule_pop/schedule_pop.cgi?UY=$UY';
WinNo='HELP4';//
W=475;
H=510;
HelpWinOpen(HELPHref1,WinNo,W,H)">$UY年の行事</a></strong></td>
EOF
$UY2 = $UY;
}
}
print <<"EOF";
        </tr>
      </table>
    </td>
  </tr>
</table>
EOF
}
#メインコンテンツ・行事日程セクション・ここまで
################################################################################
#メインコンテンツ・お問合せセクション
sub main_info {
open (IN,"../../contents/info.html");
while(<IN>){ print; }
close(IN);
}
#メインコンテンツ・お問合せセクション・ここまで
################################################################################
#メインコンテンツ・リンクセクション
sub main_link {
open (IN,"../../contents/link.html");
while(<IN>){ print; }
close(IN);
}
#メインコンテンツ・リンクセクション・ここまで
################################################################################
#メインコンテンツ・特設ページセクション
sub main_special {
  foreach $data11 (@NEW6) {
    ($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$MY,$MM,$MD,$IV,$URL) = split(/\,/,$data11);
print <<"EOF";
<table width="100%" border="0" cellspacing="3" cellpadding="0" bgcolor="#ff9933">
  <tr>
    <td>
EOF
  if ($IV eq 0) { &main_special_html; }
    elsif ($IV eq 1) {
      &main_special_tsutsuji;
    }

print <<"EOF";
    </td>
  </tr>
  <tr>
    <td align="center">
      <br>
      <TABLE width="290" cellpadding="3" cellspacing="1" bgcolor="#ffffff">
        <TBODY>
          <TR>
            <TD bgcolor="#ff9933"><B>過去の特設ページ</B></TD>
          </TR>
          <TR>
            <TD align="left">
              <TABLE border="0" cellpadding="3" cellspacing="0">
                <TBODY>
EOF
foreach $data11_2 (@NEW6_2) {
($ID,$TITLE,$UY,$UM,$UD,$EY,$EM,$ED,$MY,$MM,$MD,$IV,$URL) = split(/\,/,$data11_2);
  if ($UY ne $UY2) {
print <<"EOF";
<TR>
<TD>$UY年</TD>
<TD><B><A href="/special.html&ID=$ID" target="_self">$TITLE</A></B></TD>
</TR>
EOF
$UY2 = $UY;
  }
  else {
print <<"EOF";
<TR>
<TD></TD>
<TD><B><A href="/special.html&ID=$ID" target="_self">$TITLE</A></B></TD>
</TR>
EOF
  }
}
print <<"EOF";
</TBODY>
</TABLE></TD>
</TR>
</TBODY>
</TABLE>
<br>
</td>
</tr>
</table>
EOF
}
}
#メインコンテンツ・特設ページセクション・ここまで
################################################################################
#メインコンテンツ・特設ページ_つつじセクション
sub main_special_tsutsuji {
  @add = ("../text_data/special_tsutsuji_",$ID,".txt"); $file7 = join("",@add);
  &serch_special_tstsuji;
foreach $data13 (@NEW7) {
  ($ID_T,$TITLE_T,$UY_T,$UM_T,$UD_T,$COM_T) = split(/\,/,$data13);
  @add = ("../../images/special_tsutsuji/tsutsuji_",$ID_T,".jpg"); $grph01 = join("",@add);

print <<"EOF";
      <table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
          <td><img src="../../images/special_tsutsuji_title_01.gif" width=300 height=60></td>
        </tr>
        <tr>
          <td>
            <table width="100%" border="0" cellpadding="0" cellspacing="0" class="bgWhite">
              <tr>
                <td width="15" height="15" valign="top"><IMG SRC="../../images/special_tsutsuji_frame_01.gif" WIDTH=15 HEIGHT=15></td>
                <td>&nbsp;</td>
                <td width="15" height="15" valign="top"><IMG SRC="../../images/special_tsutsuji_frame_03.gif" WIDTH=15 HEIGHT=15></td>
              </tr>
              <tr>
                <td>&nbsp;</td>
                <td align="center">
                  <table width="100%" border="0" cellspacing="0" cellpadding="3">
                    <tr>
                      <td align="left"><h2>$UY_T年版『つつじ開花状況』</h2><hr border="1">
EOF
$pend=0;
($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$mon++;
$year = $year + 1900;
&mendymd;

if ($pend eq 1) {
print <<"EOF";
<b><font color="ff2200">※ページの更新は終了しております。また次回の掲載をお楽しみに！</font></b><br><br>
EOF
}
print <<"EOF";
このページでは、薬王寺境内のつつじを写真で紹介します。ほぼ毎日更新ですので、おいでになる時のご参考にしてください。<BR> <B><font color="#ff2200">※写真をクリックすると、大きい画像で確認できます。</font></B><BR> <HR size="1"> <B>ツツジ最新情報（$UM_T月$UD_T日）</B></td>
                    </tr>
                    <tr>
                      <td align="center">
                        <table border="0" cellpadding="0" cellspacing="1" bgcolor="#000000">
                          <tr>
                            <td class="bgWhite"><A href="javascript:function voi(){};voi()" onclick="
HELPHref1='/cgi-bin/special_tsutsuji/special_tsutsuji_popup.cgi?ID=$ID&ID_T=$ID_T';
WinNo='HELP1';//
W=627;
H=502;
HelpWinOpen(HELPHref1,WinNo,W,H)"><IMG SRC="$grph01" border="0"></a></td>
                          </tr>
                        </table>
                        <hr width="90%" size="1"> 
                      </td>
                    </tr>
                    <tr>
                      <td align="left">$COM_T</td>
                    </tr>
                    <tr>
                      <td align="center">
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                          <tr>
                            <td width="50%">
EOF
if ($FF <= 0) { ; }
else {
print <<"EOF";
<strong><a href="javascript:history.back()" target="_self">≪翌日の様子</a></strong>
EOF
}
print <<"EOF";
                            </td>
                            <td width="50%" align="right">
EOF
if ($next_num ne '') {
print <<"EOF";
<strong><A href="/special.html&ID=$ID&ID_T=all&FF=$next_num" target="_self">前日の様子≫</a></strong>
EOF
}
print <<"EOF";
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td width="15" height="15" valign="bottom"><IMG SRC="../../images/special_tsutsuji_frame_06.gif" WIDTH=15 HEIGHT=15></td>
                <td>&nbsp;</td>
                <td width="15" height="15" valign="bottom"><IMG SRC="../../images/special_tsutsuji_frame_08.gif" WIDTH=15 HEIGHT=15></td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
EOF
  }
}
#メインコンテンツ・特設ページ_つつじセクション・ここまで
################################################################################
#メインコンテンツ・特設ページ_htmlセクション
sub main_special_html {
open (IN,$URL);
while(<IN>){ print; }
close(IN);
}
#メインコンテンツ・特設ページ_htmlセクション・ここまで
################################################################################


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
