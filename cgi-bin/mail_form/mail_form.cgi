#!/usr/bin/perl
# プロバイダーのパス
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# ファイル名の設定(基本的に変更しないでください。)
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# 日本語変換コードまでのパス
require './jcode.pl';
# 送信後に表示するページ（「.html」「.shtml」「.swf」など）
$end = "./info_mail_fin.html";
# 送信文の外部ファイルまでのパス
$send_txt = "./send.txt";
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# 運営上に必要な設定です。
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# センドメールのパス
$mail_pass = '/usr/sbin/sendmail';
# 送信先メールアドレス（必ず記入してください。）
$mail_to = 'info@yakuohji.com';
# 複数にメールを送信する場合ここにアドレスを書いてください。
# 必要ない場合は「$mail_bcc = '';」に
# （アドレスとアドレスはカンマで区切ってください。）
$mail_bcc = 'hashimoto@hdg.jp,kohsei@hdg.jp';
# HTMLメールを許可する(しない＝1、する＝0)
$tag = '1';
# --+--初期設定ここまで-------------------------------------+--

# ----------------------------------------
# ここから下は変更しないでください。
# 変更するにはperlの知識が必要になります。
# ----------------------------------------
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
    else { $buffer = $ENV{'QUERY_STRING'}; }

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    
    &jcode'convert(*value,'sjis');
    
    if ($tag) {
        $value =~ s/</\&lt\;/g;
        $value =~ s/>/\&gt\;/g;
        $value =~ s/\"/\&quot\;/g;
        $value =~ s/<>/\&lt\;\&gt\;/g;
        $value =~ s/<!--(.|\n)*-->//g;
    }
    
    $FORM{$name} = $value;
    
}

print "Content-type:text/html;\n\n";

$a0 = $FORM{'a0'};
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

$ENV{'TZ'} = "JST-9";
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
$mon++;
$week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
$year += 1900;
if ($sec <10) { $sec ="0$sec";}
if ($min <10) { $min ="0$min";}
if ($hour <10) { $hour ="0$hour";}
if ($mday <10) { $mday ="0$mday";}
if ($mon <10) { $mon ="0$mon";}
$date = "$year/$mon/$mday $hour:$min ($week)";

open (IN,"$send_txt") || &error("メール送信文がありません。");
$send = join('',<IN>);
close(IN);

$send =~ s/<!--a0-->/$a0/i;
$send =~ s/<!--a1-->/$a1/i;
$send =~ s/<!--a2-->/$a2/i;
$send =~ s/<!--a3-->/$a3/i;
$send =~ s/<!--a4-->/$a4/i;
$send =~ s/<!--a5-->/$a5/i;
$send =~ s/<!--a6-->/$a6/i;
$send =~ s/<!--a7-->/$a7/i;
$send =~ s/<!--a8-->/$a8/i;
$send =~ s/<!--a9-->/$a9/i;
$send =~ s/<!--date-->/$date/i;
$send =~ s/<!--mail-->/$mail/i;

@NECESSARY = split(/,/,$necessary);
foreach (@NECESSARY) { if ($$_ eq "") { &error("未記入の欄があります。<br>すべての項目を埋めてから[送信]ボタンを押してください。"); } }

open (IN,"$send_txt") || &error("メール送信文がありません。");
$subject = <IN>;
close(IN);

	    open(MAIL,"| $mail_pass -t -f $mail_to") || &error("Can't do sendmail");
		print MAIL 'X-Mailer: LIMIT MAILER' . "\n";
        print MAIL "To: $mail_to\n";
        print MAIL "Bcc: $mail_bcc\n";
	    print MAIL "From: $mail\n";
	    print MAIL "Subject: $subject \n";
		print MAIL "Content-Transfer-Encoding: 7bit\n";
        print MAIL "Content-type: text/plain\n\n";
		print MAIL "$send\n";
	    close(MAIL);
    
open (IN,"$end");
while(<IN>){ print; }
close(IN);

exit;

sub error {

print <<"EOM";
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>七国山薬王寺</title>
<link rel="stylesheet" href="../../yakuohji_text.css" type="text/css">
</head>

<body leftmargin="3" rightmargin="0" topmargin="3" marginwidth="3" marginheight="3" color="#ffffff">
<div align="center">
  <table width="350" border="0" cellspacing="0" cellpadding="0">
    <tr> 
      <td> <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="190"><IMG SRC="../../images/mail/info_06.gif" WIDTH=190 HEIGHT=40 ALT=""></td>
            <td background="../../images/mail/info_07.gif">&nbsp;</td>
            <td width="15"><IMG SRC="../../images/mail/info_08.gif" WIDTH=15 HEIGHT=40 ALT=""></td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="25" background="../../images/mail/info_10.gif">&nbsp;</td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center"><img src="../../images/mail/mail_error_01.gif" width="300" height="100"></td>
                </tr>
                <tr>
                  <td><div align="center"> 
                      <hr width="90%" size="1">
                      <br>
                      $_[0]<BR>
                      <br>
                      <br>
                      [<A href="JavaScript:window.close()">close</A>]<br>
                    </div></td>
                </tr>
              </table></td>
            <td width="15" background="../../images/mail/info_12.gif">&nbsp;</td>
          </tr>
        </table></td>
    </tr>
    <tr> 
      <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr> 
            <td width="15"><IMG SRC="../../images/mail/info_24.gif" WIDTH=25 HEIGHT=15 ALT=""></td>
            <td background="../../images/mail/info_26.gif"><font style="font-size:1px;line-height:100%">&nbsp;</font></td>
            <td width="15"><IMG SRC="../../images/mail/info_27.gif" WIDTH=15 HEIGHT=15 ALT=""></td>
          </tr>
        </table></td>
    </tr>
  </table>
</div>
</body>
</html>


EOM

exit;

}
