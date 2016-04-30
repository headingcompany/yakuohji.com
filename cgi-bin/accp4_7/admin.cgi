#!/usr/bin/perl
################################################################################
# 高機能アクセス解析CGI Professional版 （管理者用）
# Ver 4.7
# Copyright(C) futomi 2001 - 2003
# http://www.futomi.com/
###############################################################################
use strict;
my $JFLAG;
BEGIN {
	use CGI;
	eval "use Jcode";
	if($@) {
		$JFLAG = 0;
		require './jcode.pl';
	} else {
		$JFLAG = 1;
	}
}
my $q = new CGI;
$| = 1;
#CGIの設定
my $FREE_SERVER_NAME = '\.tok2\.com|\.infoseek\.co\.jp|\.xrea\.com';

my $COPYRIGHT = '<a href="http://www.futomi.com/" target="_blank">futomi\'s CGI Cafe</a>';
my $COOKIE_NAME = 'accadminpass';
my $RESTRICT_COOKIE_NAME = 'accrestrict';
my $CONF_DATA = './data/config.cgi';
my $HELP_DATA = './data/help.dat';
my $SETPASS_TMPL = './template/admin.setpass.html';
my $COMPLETE_TMPL = './template/admin.complete.html';
my $CONF_TMPL = './template/admin.conf.html';
my $AUTH_TMPL = './template/admin.auth.html';
my $HELP_TMPL = './template/admin.help.html';
my $SYSCHECK_TMPL = './template/admin.syscheck.html';
my $LOGINFO_TMPL = './template/admin.loginfo.html';
my $RESTRICT1_TMPL = './template/admin.restrict1.html';
my $RESTRICT2_TMPL = './template/admin.restrict2.html';

my @CONF_KEYS = (
	'ADMINPASS',		#管理者用パスワード
	'IMAGE_URL',		#イメージディレクトリの URL
	'AUTHFLAG',		#アクセス制限機能
	'PASSWORD',		#パスワード
	'URL2PATH_FLAG',	#URLマッピング機能
	'URL2PATH_URL',		#URLマッピング（URL）
	'URL2PATH_PATH',	#URLマッピング（パス）
	'TIMEDIFF',		#時差の調整
	'GRAPHMAXLENGTH',	#棒グラフの長さ
	'ROW',			#表示ランキング数
	'LOTATION',		#ローテーション設定
	'LOTATION_SIZE',	#ローテーションサイズ
	'LOTATION_SAVE',	#過去ログ保存機能
	'MY_SITE_URLs',		#リンク元除外URL
	'REJECT_HOSTS',		#ロギング除外ホスト
	'DIRECTORYINDEX',	#ディレクトリインデックス
	'URLHANDLE',		#アクセスページ URL の扱い
	'USECOOKIE',		#Cookieの利用設定
	'EXPIREDAYS',		#Cookieの有効期限
	'INTERVAL',		#セッションインターバル
	'LOCK_FLAG',		#ログファイルのロック処理
	'CIRCLE_GLAPH',		#円グラフの方式
	'IMAGE_TYPE'		#解析タグの表示画像形式
);

my $err_status = '<font color="RED">NG</font>';
my $ok_status = '<font color="GREEN">OK</font>';

#ログ格納ディレクトリ
my $LOGDIR = './logs';

#設定データ取得
my %CONF = &GetConf($CONF_DATA);

#処理内容の取得
my $action = $q->param('action');
my $setpass_flag = $q->param('setpass');

#パスワード設定フラグが「1」なら、パスワード設定処理
if($setpass_flag) {
	&SetPass;
	%CONF = &GetConf($CONF_DATA);
}
#パスワードが設定されていなければ、パスワード設定画面を表示
unless($CONF{'ADMINPASS'}) {
	&PrintTemplate($SETPASS_TMPL);
	exit;
}
#認証
unless($setpass_flag) {
	unless(&Auth) {
		&ErrorPrint("パスワードが違います。");
	}
}
#処理分岐
if($action eq 'conf') {
	&PrintConf($CONF_TMPL);
} elsif($action eq 'setconf') {
	&SetConf;
	&PrintTemplate($COMPLETE_TMPL, '設定完了しました。', 'admin.cgi?action=conf');
} elsif($action eq 'system') {
	&PrintSysCheck($SYSCHECK_TMPL);
} elsif($action eq 'syscheck') {
	&SysCheck;
} elsif($action eq 'help') {
	my $item = $q->param('item');
	&PrintHelp($item);
} elsif($action eq 'log') {
	&PrintLogInfo;
} elsif($action eq 'logdel') {
	my $file = $q->param('file');
	my $log = "$LOGDIR/$file";
	&DeleteLogFile($log);
	&PrintLogInfo;
} elsif($action eq 'download') {
	my $file = $q->param('file');
	&DownloadFile($file);
} elsif($action eq 'restrict') {
	&PrintRestrictForm;
} elsif($action eq 'restrictset') {
	&SetRestrictCookie;
} elsif($action eq 'restrictclear') {
	&ClearRestrictCookie;
} else {
	&PrintSysCheck($SYSCHECK_TMPL);
}

exit;
my($title, $result, $status);


format STDOUT =
@<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< : @<<<<<<<<<<<<<<<<<<<<<<< : @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
$title,$result,$status
.


sub ClearRestrictCookie {
	my $html;
	$html .= "<html><head>\n";
	$html .= "<meta http-equiv=\"Content-Language\" content=\"ja\">\n";
	$html .= "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=shift_jis\">\n";
	$html .= "\$COOKIE\$\n";
	$html .= "<title> </title>\n";
	$html .= "</head>\n";
	$html .= "<body bgcolor=\"#FFFFFF\">\n";
	$html .= "<center>\n";
	$html .= "<div style=\"font-size: 12px\">設定を解除しました。</div>\n";
	$html .= "</center>\n";
	$html .= "</body></html>\n";

	if($ENV{'SERVER_NAME'} =~ /($FREE_SERVER_NAME)/) {
		$html =~ s/\$COOKIE\$/<META HTTP-EQUIV='Set-Cookie' CONTENT='$RESTRICT_COOKIE_NAME=clear;expires=Thu, 01-Jan-1970 00:00:00 GMT;'>/;
	} else {
		$html =~ s/\$COOKIE\$//;
		my $CookieHeaderString = &ClearCookie($RESTRICT_COOKIE_NAME);
		print "P3P: CP=\"NOI TAIa\"\n";
		print "$CookieHeaderString\n";
	}
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
	exit;
}

sub SetRestrictCookie {
	my $html;
	$html .= "<html><head>\n";
	$html .= "<meta http-equiv=\"Content-Language\" content=\"ja\">\n";
	$html .= "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=shift_jis\">\n";
	$html .= "\$COOKIE\$\n";
	$html .= "<title> </title>\n";
	$html .= "</head>\n";
	$html .= "<body bgcolor=\"#FFFFFF\">\n";
	$html .= "<center>\n";
	$html .= "<div style=\"font-size: 12px\">設定完了しました。</div>\n";
	$html .= "</center>\n";
	$html .= "</body></html>\n";
	my $expire = time + 315360000;	#10年後
	my $CookieHeaderString = &SetCookie($RESTRICT_COOKIE_NAME, '1', $expire);
	if($ENV{'SERVER_NAME'} =~ /($FREE_SERVER_NAME)/) {
		my $content_str = $CookieHeaderString;
		$content_str =~ s/^Set-Cookie: //;
		$html =~ s/\$COOKIE\$/<META HTTP-EQUIV='Set-Cookie' CONTENT='$content_str'>/;
	} else {
		$html =~ s/\$COOKIE\$//;
		print "P3P: CP=\"NOI TAIa\"\n";
		print "$CookieHeaderString\n";
	}
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
	exit;
}

sub PrintRestrictForm {
	my %cookie = &GetCookie;
	my $template;
	if($cookie{$RESTRICT_COOKIE_NAME}) {
		$template = $RESTRICT2_TMPL;
	} else {
		$template = $RESTRICT1_TMPL;
	}
	my $html = &ReadTemplate($template);
	if($ENV{'SERVER_NAME'} =~ /($FREE_SERVER_NAME)/) {
		$html =~ s/\$COOKIE\$/<META HTTP-EQUIV='Set-Cookie' CONTENT='$COOKIE_NAME=$CONF{'ADMINPASS'};'>/;
	} else {
		$html =~ s/\$COOKIE\$//;
		my $CookieHeaderString = &SetCookie($COOKIE_NAME, $CONF{'ADMINPASS'});
		print "P3P: CP=\"NOI TAIa\"\n";
		print "$CookieHeaderString\n";
	}
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
	exit;
}


sub DownloadFile {
	my($file) = @_;
	my $log = "$LOGDIR/$file";
	my $ua = $ENV{'HTTP_USER_AGENT'};
	my $rc = "\x0A";	#LF
	if($ua =~ /Windows|Win32|Win 9x/) {
		$rc = "\x0D\x0A";	#CRLF
	} elsif($ua =~ /Macintosh|Mac_/) {
		$rc = "\x0D";	#CR
	}
	my $size = -s $log;
	open(LOG, "$log") || &ErrorPrint("ログファイル <tt>$log</tt> をオープンできませんでした。 : $!");
	my $contents;
	sysread(LOG, $contents, $size);
	close(LOG);
	$contents =~ s/\n/$rc/g;
	#print "Content-Type: application/octet-stream\n";
	print "Content-Disposition: attachment; filename=$file\n";
	print "Content-length: $size\n";
	print "\n";
	print "$contents";
	exit;
}

sub DeleteLogFile {
	my($log) = @_;
	unless(unlink($log)) {
		&ErrorPrint("ログファイル $log を削除できませんでした。 : $!");
	}
}

sub PrintLogInfo {
	opendir(DIR, "$LOGDIR") || &ErrorPrint("ログ格納ディレクトリ「$LOGDIR」をオープンできませんでした。");
	my @files = readdir(DIR);
	closedir(DIR);
	my @logs = ();
	for my $file (@files) {
		if($file =~ /^access_log/) {
			push(@logs, $file);
		}
	}
	my(%size_list, %mtime_list);
	for my $file (@logs) {
		my @stat = stat("$LOGDIR/$file");
		$size_list{$file} = $stat[7];
		$mtime_list{$file} = $stat[9];
	}
	my $list;
	foreach my $file (ValueSort(\%mtime_list)) {
		my $date = &ConvEpoc2Date($mtime_list{$file});
		my $dsp_size = &CommaFormat($size_list{$file});
		$list .= "  <tr>\n";
		$list .= "    <td class=\"ListHeader4\">$file</td>\n";	#ファイル名
		$list .= "    <td class=\"ListHeader4\" align=\"right\">$dsp_size byte</td>\n";	#サイズ
		$list .= "    <td class=\"ListHeader4\">$date</td>\n";	#最終更新日時
		$list .= "    <td class=\"ListHeader4\" align=\"center\"><a href=\"admin.cgi?action=download&file=$file\">Download</a></td>\n";	#ダウンロード
		$list .= "    <td class=\"ListHeader4\" align=\"center\"><a href=\"javascript:delConfirm('$file')\">削除</a></td>\n";	#削除
		$list .= "  </tr>\n";
	}
	my $html = &ReadTemplate($LOGINFO_TMPL);
	$html =~ s/\$LIST\$/$list/;
	if($ENV{'SERVER_NAME'} =~ /($FREE_SERVER_NAME)/) {
		$html =~ s/\$COOKIE\$/<META HTTP-EQUIV='Set-Cookie' CONTENT='$COOKIE_NAME=$CONF{'ADMINPASS'};'>/;
	} else {
		$html =~ s/\$COOKIE\$//;
		my $CookieHeaderString = &SetCookie($COOKIE_NAME, $CONF{'ADMINPASS'});
		print "P3P: CP=\"NOI TAIa\"\n";
		print "$CookieHeaderString\n";
	}
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
	exit;
}

sub PrintSysCheck {
	my($file) = @_;
	my $size = -s $file;
	if(!open(IN, "$file")) {
		&ErrorPrint("テンプレートファイル <tt>$file</tt> をオープンできませんでした。 : $!");
		exit;
	}
	binmode(IN);
	my $filestr;
	sysread(IN, $filestr, $size);
	close(IN);
	my $key;
	$filestr =~ s/\$COPYRIGHT\$/$COPYRIGHT/g;
	if($ENV{'SERVER_NAME'} =~ /($FREE_SERVER_NAME)/) {
		$filestr =~ s/\$COOKIE\$/<META HTTP-EQUIV='Set-Cookie' CONTENT='$COOKIE_NAME=$CONF{'ADMINPASS'};'>/;
	} else {
		$filestr =~ s/\$COOKIE\$//;
		my $CookieHeaderString = &SetCookie($COOKIE_NAME, $CONF{'ADMINPASS'});
		print "P3P: CP=\"NOI TAIa\"\n";
		print "$CookieHeaderString\n";
	}
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$filestr\n";
	exit;
}


sub SysCheckError {
	my($str) = @_;
	my $err = "<blockquote>\n";
	$err .= "<table border=\"0\" width=\"500\"><tr><td>\n";
	$err .= "<div><font color=\"RED\"><tt>\n";
	$err .= "$str\n";
	$err .= "</tt></font></div>\n";
	$err .= "</td></tr></table>\n";
	$err .= "</blockquote>\n";
	return $err;
}

sub SysCheck {
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "<html>\n";
	print "<head>\n";
	print "  <meta http-equiv=\"Content-Language\" content=\"ja\">\n";
	print "  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=shift_jis\">\n";
	print "  <style type=\"text/css\">\n";
	print "    div {font-size: 12px;}\n";
	print "  </style>\n";
	print "  <title>futomi's CGI Cafe - 高機能アクセス解析 CGI Professional Edition</title>\n";
	print "</head>\n\n";
	print "<body bgcolor=\"#FFFFFF\">\n";
	print "<br>\n";
	print "<br>\n";

	print "<div>システム診断を開始します。問題がある場合には、赤字で表\示されます。診断が完了するまでしばらくお待ちください。</div>\n";
	print "<hr>\n";

	print "<div>\n";
	print "<pre><tt>\n";
	sleep 1;

	$title = '■ 日本語変換ライブラリー';
	if($JFLAG) {
		$result = 'Jcode.pm';
		$status = '';
	} else {
		$result = 'jcode.pl';
		$status = '';
	}
	write();

	my $ex_uid = $>;
	my @stats = stat("./admin.cgi");
	my $owner_uid = $stats[4];
	my $executer;
	if($ex_uid eq $owner_uid) {
		$executer = 'owner';
	} else {
		$executer = 'other';
	}
	$title = "■ CGI の実行権限";
	$result = "$executer";
	$status = "";
	write();

	print "\n";

	my $rc = &GetReturnCode("./admin.cgi");
	$title = "■ CGI ファイル ./admin.cgi の改行コード";
	$result = "$rc";
	$status = "";
	write();

	my $perl_path = &GetPerlPath("./admin.cgi");
	$title = "■ CGI ファイル ./admin.cgi の Perl パス";
	$result = "$perl_path";
	$status = "";
	write();

	my $permission = sprintf("%o",(stat("./admin.cgi"))[2] & 0777);
	$title = "■ CGI ファイル ./admin.cgi のパーミッション";
	$result = "$permission";
	$status = "";
	write();
	print "\n";

	&ExistCheck('./acclog.cgi', 'CGI ファイル');
	&ReturnCodeCheck('./acclog.cgi', 'CGI ファイル', $rc);
	&PerlPathCheck('./acclog.cgi', $perl_path);
	&PermissionCheck('./acclog.cgi', $executer, $permission);
	print "\n";

	&ExistCheck('./acc.cgi', 'CGI ファイル');
	&ReturnCodeCheck('./acc.cgi', 'CGI ファイル', $rc);
	&PerlPathCheck('./acc.cgi', $perl_path);
	&PermissionCheck('./acc.cgi', $executer, $permission);
	print "\n";

	&ExistCheck('./jcode.pl', '文字コード変換ライブラリー');
	&ReturnCodeCheck('./jcode.pl', '文字コード変換ライブラリー', $rc);
	print "\n";

	&ExistCheck('./acclogo.gif', '解析時表示用画像ファイル');
	&ExistCheck('./acclogo.png', '解析時表示用画像ファイル');
	&ExistCheck('./acclogo.jpg', '解析時表示用画像ファイル');
	print "\n";

	&DirExistCheck('./logs', 'ログ格納ディレクトリ');
	&DirWriteCheck('./logs', 'ログ格納ディレクトリ');
	print "\n";

	&DirExistCheck('./data', '各種データ格納ディレクトリ');
	&ExistCheck('./data/config.cgi', 'CGI 設定ファイル');
	&ReturnCodeCheck('./data/config.cgi', 'CGI 設定ファイル', $rc);
	&WriteCheck('./data/config.cgi', 'CGI 設定ファイル');
	&ExistCheck('./data/country_code.dat', '国コード定義ファイル');
	&ReturnCodeCheck('./data/country_code.dat', '国コード定義ファイル', $rc);
	&ExistCheck('./data/help.dat', 'ヘルプファイル');
	&ReturnCodeCheck('./data/help.dat', 'ヘルプファイル', $rc);
	&ExistCheck('./data/language.dat', '言語定義ファイル');
	&ReturnCodeCheck('./data/language.dat', '言語定義ファイル', $rc);
	&ExistCheck('./data/organization.dat', '組織名定義ファイル');
	&ReturnCodeCheck('./data/organization.dat', '組織名定義ファイル', $rc);
	&ExistCheck('./data/pref.dat', '都道府県定義ファイル');
	&ReturnCodeCheck('./data/pref.dat', '都道府県定義ファイル', $rc);
	&ExistCheck('./data/site.dat', 'サイト名定義ファイル');
	&ReturnCodeCheck('./data/site.dat', 'サイト名定義ファイル', $rc);
	&ExistCheck('./data/ipaddr.dat', 'IPアドレス定義ファイル');
	&ReturnCodeCheck('./data/ipaddr.dat', 'IPアドレス定義ファイル', $rc);
	&ExistCheck('./data/title.dat', 'タイトル定義ファイル');
	&ReturnCodeCheck('./data/title.dat', 'タイトル定義ファイル', $rc);

	print "\n";

	&DirExistCheck('./template', 'テンプレートファイル格納ディレクトリ');
	&ExistCheck('./template/admin.auth.html');
	&ExistCheck('./template/admin.complete.html');
	&ExistCheck('./template/admin.conf.html');
	&ExistCheck('./template/admin.help.html');
	&ExistCheck('./template/admin.loginfo.html');
	&ExistCheck('./template/admin.restrict1.html');
	&ExistCheck('./template/admin.restrict2.html');
	&ExistCheck('./template/admin.setpass.html');
	&ExistCheck('./template/admin.syscheck.html');
	&ExistCheck('./template/loginfo.html');
	&ExistCheck('./template/logon.html');
	&ExistCheck('./template/mainframe.html');
	&ExistCheck('./template/menuframe.html');
	&ExistCheck('./template/menuframe_ie.html');
	&ExistCheck('./template/result.html');
	&ExistCheck('./template/search.html');
	print $q->hr;
	print "診断完了<br>\n";
	print "</tt></pre>\n";
	print "</body>\n";
	print "</html>\n\n";
}

sub PermissionCheck {
	my($file, , $executer, $permission) = @_;
	my $permission2 = sprintf("%o",(stat("$file"))[2] & 0777);
	$title = "■ CGI ファイル $file の パーミッション";
	$result = "$permission2";
	my $err_str;
	my $err_flag = 0;
	if($permission2 eq '0' || $permission2 eq '') {
		$result = "診断不可";
		$status = "";
	} elsif($permission eq $permission2) {
		$status = $ok_status;
	} else {
		if($executer eq 'owner') {
			unless($permission2 =~ /^(7|5)/) {
				$err_str = &SysCheckError("$file の $executer に実行権限がありません。パーミッションを $permission のように $executer に実行権を与えるように設定してください。");
				$status = $err_status;
				$err_flag = 1;
			} else {
				$status = $ok_status;
			}
		} elsif($executer eq 'other') {
			unless($permission2 =~ /(7|5)$/) {
				$err_str = &SysCheckError("$file の $executer に実行権限がありません。パーミッションを $permission のように $executer に実行権を与えるように設定してください。");
				$status = $err_status;
				$err_flag = 1;
			} else {
				$status = $ok_status;
			}
		}
	}
	write();
	if($err_flag) {
		print "$err_str\n";
	}
}

sub PerlPathCheck {
	my($file, $perl_path) = @_;
	my $perl_path2 = &GetPerlPath("$file");
	$title = "■ CGI ファイル $file の Perl パス設定";
	$result = "$perl_path2";
	my $err_flag = 0;
	my $err_str;
	if($perl_path eq '' || $perl_path2 eq '') {
		$result = "診断不可";
		$status = "";
	} elsif($perl_path2 eq $perl_path) {
		$status = $ok_status;
	} else {
		$err_str = &SysCheckError("$file の Perl パスが正しく設定されていません。$file の 1 行目を「$perl_path」に書き換えてください。");
		$err_flag = 1;
		$status = $err_status;
	}
	write();
	if($err_flag) {
		print "$err_str\n";
	}
}

sub WriteCheck {
	my($file, $str) = @_;
	$title = "■ $str $file への書込みチェック";
	$result = "";
	my $err_flag = 0;
	my $err_str;
	if(open(FILE, ">>$file")) {
		$status = $ok_status;
		close(FILE);
	} else {
		$status = $err_status;
		$err_flag = 1;
		$err_str = &SysCheckError("$file のパーミッションが正しくありません。606 もしくは 666 に変更してください。");
	}
	write();
	if($err_flag) {
		print "$err_str\n";
	}
}

sub DirWriteCheck {
	my($dir, $str) = @_;
	my $test_file = "$dir/check.txt";
	$title = "■ $str $dir 内のファイル書込みチェック";
	$result = sprintf("%o",(stat("$dir"))[2] & 0777);
	my $err_flag = 0;
	my $err_str;
	if(-e "$dir") {
		if(open(TEST, ">$test_file")) {
			$status = $ok_status;
			close(TEST);
			unlink("$test_file");
		} else {
			$status = $err_status;
			$err_str = &SysCheckError("ディレクトリ $dir のパーミッションが正しくありません。707 もしくは 777 に変更してください。");
			$err_flag = 1;
		}
		write();
		if($err_flag) {
			print "$err_str\n";
		}
	} else {
		$result = "診断不可";
		$status = "";
		write();
	}
}

sub DirExistCheck {
	my($dir, $str) = @_;
	$title = "■ $str $dir の存在";
	$result = "";
	my $err_flag = 0;
	my $err_str;

	if(opendir(DIR, "$dir")) {
		$status = $ok_status;
		closedir(DIR);
	} else {
		$status = $err_status;
		$err_flag = 1;
		$err_str = &SysCheckError("ディレクトリ $dir がありません。サーバ上に $dir を作成してください。");
	}
	write();
	if($err_flag) {
		print "$err_str\n";
	}
}

sub ExistCheck {
	my($file, $str) = @_;
	$title = "■ $str $file の存在";
	$result = "";
	my $err_flag = 0;
	my $err_str;
	if(-e "$file") {
		$status = $ok_status;
	} else {
		$err_flag = 1;
		$status = $err_status;
		$err_str = &SysCheckError("$file がありません。サーバに $file を アップロードしてください。");
	}
	write();
	if($err_flag) {
		print "$err_str\n";
	}
}

sub ReturnCodeCheck {
	my($file, $str, $rc) = @_;
	my $rc2 = &GetReturnCode("$file");
	$title = "■ $str $file の改行コード";
	$result = "$rc2";
	my $err_flag = 0;
	my $err_str;
	if($rc2 eq '' || $rc eq '') {
		$result = "診断不可";
		$status = "";
	} elsif($rc2 eq $rc) {
		$status = $ok_status;
	} else {
		$status = $err_status;
		$err_flag = 1;
		$err_str = &SysCheckError("$file の改行コードが正しくありません。$file を ASCII モードで上書きアップロードしてください。");
	}
	write();
	if($err_flag) {
		print "$err_str\n";
	}
}

sub GetPerlPath {
	my($file) = @_;
	if(open(FILE, "$file")) {
		my @lines = <FILE>;
		my $perl_path = shift @lines;
		chop $perl_path;
		close(FILE);
		return $perl_path;
	} else {
		return '';
	}
}

sub PrintHelp {
	my($item) = @_;

	my $size = -s $HELP_DATA;
	if(!open(IN, "$HELP_DATA")) {
		&ErrorPrint("ヘルプファイル <tt>$HELP_DATA</tt> をオープンできませんでした。 : $!");
		exit;
	}
	binmode(IN);
	my $helpstr;
	sysread(IN, $helpstr, $size);
	close(IN);
	$helpstr = &UnifyReturnCode($helpstr);
	my @help_parts = split(/<-- delimiter -->/, $helpstr);
	my %help = ();
	my %itemname = ();
	my $part;
	for $part (@help_parts) {
		$part =~ s/^(\n|\s)+//;
		my @lines = split(/\n/, $part);
		my $key = shift(@lines);
		my $keyname = shift(@lines);
		my $help_str = join("\n", @lines);
		$help{$key} = $help_str;
		$itemname{$key} = $keyname;
	}

	$size = -s $HELP_TMPL;
	if(!open(IN, "$HELP_TMPL")) {
		&ErrorPrint("テンプレートファイル <tt>$HELP_TMPL</tt> をオープンできませんでした。 : $!");
		exit;
	}
	binmode(IN);
	my $filestr;
	sysread(IN, $filestr, $size);
	close(IN);
	$filestr =~ s/\$HELP\$/$help{$item}/g;
	$filestr =~ s/\$ITEM\$/$itemname{$item}/g;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$filestr\n";
	exit;
}


sub SetConf {
	my $IMAGE_URL = $q->param('IMAGE_URL');
	if($IMAGE_URL) {
		if($IMAGE_URL =~ /\/$/) {
			&ErrorPrint("イメージディレクトリの URL の最後にスラッシュは入れないで下さい。");
		}
		$CONF{'IMAGE_URL'} = $IMAGE_URL;
	} else {
		&ErrorPrint("イメージディレクトリの URL を指定して下さい。");
	}

	my $AUTHFLAG = $q->param('AUTHFLAG');
	my $PASSWORD = $q->param('PASSWORD');
	$CONF{'AUTHFLAG'} = $AUTHFLAG;
	if($AUTHFLAG) {
		if($PASSWORD eq "") {
			&ErrorPrint("パスワードを指定して下さい。");
		} else {
			if($PASSWORD =~ /[^a-zA-Z0-9\-\_]/) {
				&ErrorPrint("パスワードは、半角英数字、半角ハイフン、半角アンダースコアのみで指定して下さい。");
			}
			$CONF{'PASSWORD'} = $PASSWORD;
		}
	}

	my $URL2PATH_FLAG = $q->param('URL2PATH_FLAG');
	my $URL2PATH_URL = $q->param('URL2PATH_URL');
	my $URL2PATH_PATH = $q->param('URL2PATH_PATH');
	$CONF{'URL2PATH_FLAG'} = $URL2PATH_FLAG;
	if($URL2PATH_FLAG) {
		if($URL2PATH_URL eq "") {
			&ErrorPrint("URL マッピング機能\を使う場合には、マッピング元となる URL を指定して下さい。");
		}
		if($URL2PATH_PATH eq "") {
			&ErrorPrint("URL マッピング機能\を使う場合には、マッピング先となる パス を指定して下さい。");
		}
		unless($URL2PATH_URL =~ /\/$/) {
			&ErrorPrint("URL マッピングの指定では、最後にスラッシュを入れてください。");
		}
		unless($URL2PATH_PATH =~ /\/$/) {
			&ErrorPrint("URL マッピングの指定では、最後にスラッシュを入れてください。");
		}
		if(opendir(DIR, "$URL2PATH_PATH")) {
			closedir(DIR);
		} else {
			&ErrorPrint("URL マッピングの設定において、マッピング先のパスは存在しません。: $!");
		}
		$CONF{'URL2PATH_URL'} = $URL2PATH_URL;
		$CONF{'URL2PATH_PATH'} = $URL2PATH_PATH;
	}

	my $TIMEDIFF = $q->param('TIMEDIFF');
	unless($TIMEDIFF =~ /^\-*[0-9]+$/) {
		&ErrorPrint("時差の調整は、半角数字のみで指定して下さい。");
	}
	$TIMEDIFF =~ s/^0*//;
	if($TIMEDIFF eq "") {
		$TIMEDIFF = 0;
	}
	$CONF{'TIMEDIFF'} = $TIMEDIFF;

	my $GRAPHMAXLENGTH = $q->param('GRAPHMAXLENGTH');
	if($GRAPHMAXLENGTH =~ /[^0-9]/) {
		&ErrorPrint("棒グラフの長さは、半角数字のみで指定して下さい。");
	}
	$GRAPHMAXLENGTH =~ s/^0*//;
	if($GRAPHMAXLENGTH eq "") {
		$GRAPHMAXLENGTH = 0;
	}
	$CONF{'GRAPHMAXLENGTH'} = $GRAPHMAXLENGTH;

	my $ROW = $q->param('ROW');
	if($ROW =~ /[^0-9]/) {
		&ErrorPrint("ランキング表示数は、半角数字のみで指定して下さい。");
	}
	$ROW =~ s/^0*//;
	if($ROW eq "") {
		$ROW = 0;
	}
	$CONF{'ROW'} = $ROW;

	my $LOTATION = $q->param('LOTATION');
	my $LOTATION_SIZE = $q->param('LOTATION_SIZE');
	my $LOTATION_SAVE = $q->param('LOTATION_SAVE');
	$CONF{'LOTATION'} = $LOTATION;
	if($LOTATION eq "1") {
		my $LOTATION_SIZE = $q->param('LOTATION_SIZE');
		if($LOTATION_SIZE eq "") {
			&ErrorPrint("ローテーションサイズを指定して下さい。");
		}
		if($LOTATION_SIZE =~ /[^0-9]/) {
			&ErrorPrint("ローテーションサイズは、半角数字のみで指定して下さい。");
		}
		$LOTATION_SIZE =~ s/^0*//;
		if($LOTATION_SIZE <= 0) {
			&ErrorPrint("ローテーションサイズに 0 以下は指定できません。");
		}
		$CONF{'LOTATION_SIZE'} = $LOTATION_SIZE;
	}
	if($LOTATION > 0) {
		$CONF{'LOTATION_SAVE'} = $LOTATION_SAVE;
	}

	my $MY_SITE_URLs = $q->param('MY_SITE_URLs');
	$MY_SITE_URLs = &UnifyReturnCode($MY_SITE_URLs);
	my @sites = split(/\n/, $MY_SITE_URLs);
	my $site;
	for $site (@sites) {
		unless($site =~ /https*:\/\//) {
			&ErrorPrint("リンク元解析 除外 URL の指定は、<tt>http://</tt> から指定して下さい。 : <tt>$site</tt>");
		}
		if($site =~ /[^a-zA-Z0-9\-\_\.\%\:\/\~\&\=\?]/) {
			&ErrorPrint("除外ホストの指定で、不適切な文字が含まれています。 : <tt>$site</tt>");
		}
	}
	$MY_SITE_URLs =~ s/\n/,/g;
	$CONF{'MY_SITE_URLs'} = $MY_SITE_URLs;

	my $REJECT_HOSTS = $q->param('REJECT_HOSTS');
	$REJECT_HOSTS = &UnifyReturnCode($REJECT_HOSTS);
	my @hosts = split(/\n/, $REJECT_HOSTS);
	my $host;
	for $host (@hosts) {
		if($host =~ /https*:\/\//) {
			&ErrorPrint("除外ホストの指定では、<tt>http://</tt> から指定できません。: <tt>$host</tt>");
		}
		if($host =~ /[^a-zA-Z0-9\-\_\.]/) {
			&ErrorPrint("除外ホストの指定で、不適切な文字が含まれています。 : <tt>$host</tt>");
		}
	}
	$REJECT_HOSTS =~ s/\n/,/g;
	$CONF{'REJECT_HOSTS'} = $REJECT_HOSTS;

	my $DIRECTORYINDEX = $q->param('DIRECTORYINDEX');
	$DIRECTORYINDEX = &UnifyReturnCode($DIRECTORYINDEX);
	$DIRECTORYINDEX =~ s/\n/,/g;
	$CONF{'DIRECTORYINDEX'} = $DIRECTORYINDEX;

	$CONF{'URLHANDLE'} = $q->param('URLHANDLE');

	my $USECOOKIE = $q->param('USECOOKIE');
	my $EXPIREDAYS = $q->param('EXPIREDAYS');
	$CONF{'USECOOKIE'} = $USECOOKIE;
	if($USECOOKIE) {
		if($EXPIREDAYS eq "") {
			&ErrorPrint("Cookie 有効期限を指定して下さい。");
		}
		if($EXPIREDAYS =~ /[^0-9]/) {
			&ErrorPrint("Cookie 有効期限は、半角数字のみで指定して下さい。");
		}
		$EXPIREDAYS =~ s/^0*//;
		if($EXPIREDAYS <= 0) {
			&ErrorPrint("Cookie 有効期限に 0 以下は指定できません。");
		}
		$CONF{'EXPIREDAYS'} = $EXPIREDAYS;
	}

	my $INTERVAL = $q->param('INTERVAL');
	if($INTERVAL eq "") {
		&ErrorPrint("セッションインターバルを指定して下さい。");
	}
	if($INTERVAL =~ /[^0-9]/) {
		&ErrorPrint("セッションインターバルは、半角数字のみで指定して下さい。");
	}
	$INTERVAL =~ s/^0*//;
	if($INTERVAL <= 0) {
		&ErrorPrint("セッションインターバルに 0 以下は指定できません。");
	}
	$CONF{'INTERVAL'} = $INTERVAL;
	$CONF{'LOCK_FLAG'} = $q->param('LOCK_FLAG');
	$CONF{'CIRCLE_GLAPH'} = $q->param('CIRCLE_GLAPH');
	$CONF{'IMAGE_TYPE'} = $q->param('IMAGE_TYPE');
	&WriteConfData;
}

sub PrintConf {
	my($file) = @_;
	my $size = -s $file;
	if(!open(IN, "$file")) {
		&ErrorPrint("テンプレートファイル <tt>$file</tt> をオープンできませんでした。 : $!");
		exit;
	}
	binmode(IN);
	my $filestr;
	sysread(IN, $filestr, $size);
	close(IN);
	my $key;
	for $key (@CONF_KEYS) {
		if($key =~ /^(AUTHFLAG|URL2PATH_FLAG|LOTATION|LOTATION_SAVE|USECOOKIE|URLHANDLE|LOCK_FLAG|CIRCLE_GLAPH|IMAGE_TYPE)$/) {
			$filestr =~ s/\$$key$CONF{$key}\$/selected/g;
			$filestr =~ s/\$$key[0-9]+\$//g;
		} elsif($key =~ /^(MY_SITE_URLs|REJECT_HOSTS|DIRECTORYINDEX)$/) {
			my @items = split(/,/, $CONF{$key});
			my $tmp = join("\n", @items);
			$filestr =~ s/\$$key\$/$tmp/g;
		} else {
			$filestr =~ s/\$$key\$/$CONF{$key}/g;
		}
	}
	$filestr =~ s/\$COPYRIGHT\$/$COPYRIGHT/g;
	if($ENV{'SERVER_NAME'} =~ /($FREE_SERVER_NAME)/) {
		$filestr =~ s/\$COOKIE\$/<META HTTP-EQUIV='Set-Cookie' CONTENT='$COOKIE_NAME=$CONF{'ADMINPASS'};'>/;
	} else {
		$filestr =~ s/\$COOKIE\$//;
		my $CookieHeaderString = &SetCookie($COOKIE_NAME, $CONF{'ADMINPASS'});
		print "P3P: CP=\"NOI TAIa\"\n";
		print "$CookieHeaderString\n";
	}
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$filestr\n";
	exit;
}

sub Auth {
	my %cookie = &GetCookie;
	my $cookie_pass = $cookie{$COOKIE_NAME};
	my $in_pass = $q->param('pass');
	my($pass);
	if($cookie_pass) {
		$pass = $cookie_pass;
	} elsif($in_pass) {
		my $salt;
		if($CONF{'ADMINPASS'} =~ /^\$1\$([^\$]+)\$/) {
			$salt = $1;
		} else {
			$salt = substr($CONF{'ADMINPASS'}, 0, 2);
		}
		$pass = crypt($in_pass, $salt);
	} else {
		&PrintTemplate($AUTH_TMPL);
	}
	if($pass eq $CONF{'ADMINPASS'}) {
		return 1;
	} else {
		return 0;
	}
}

sub SetPass {
	my $pass1 = $q->param('PASSWORD1');
	my $pass2 = $q->param('PASSWORD2');
	unless($pass1 && $pass2) {
		&ErrorPrint("パスワードを指定してください。");
	}
	unless($pass1 eq $pass2) {
		&ErrorPrint("パスワード再入力が間違っています。再度注意して入力してください。");
	}
	if($pass1 =~ /[^a-zA-Z0-9\-\_]/) {
		&ErrorPrint("パスワードに不正な文字が含まれています。指定できる文字は、半角の英数、ハイフン、アンダースコアです。");
	}
	my $enc_pass = &EncryptPasswd($pass1);
	$CONF{'ADMINPASS'} = "$enc_pass";
	&WriteConfData;
}

sub PrintTemplate {
	my($file, $message, $back_link) = @_;
	my $size = -s $file;
	if(!open(IN, "$file")) {
		&ErrorPrint("テンプレートファイル <tt>$file</tt> をオープンできませんでした。 : $!");
		exit;
	}
	binmode(IN);
	my $filestr;
	sysread(IN, $filestr, $size);
	close(IN);
	my $key;
	for $key (keys %CONF) {
		$filestr =~ s/\$$key\$/$CONF{$key}/g;
	}
	$filestr =~ s/\$BACK\$/$back_link/g;
	$filestr =~ s/\$MESSAGE\$/$message/g;
	$filestr =~ s/\$COPYRIGHT\$/$COPYRIGHT/g;
	$filestr =~ s/\$ACTION\$/$action/g;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$filestr\n";
	exit;
}

sub GetConf {
	my($file) = @_;
	my %data = ();
	open(FILE, "$file") || &ErrorPrint("設定ファイル <tt>$file</tt> をオープンできませんでした。: $!");
	while(<FILE>) {
		chop;
		if(/^([a-zA-Z0-9\_\-]+)\=(.+)$/) {
			my $key = $1;
			my $value = $2;
			unless($key) {next;}
			$key =~ s/^[\s\t]*//;
			$key =~ s/[\s\t]*$//;
			$value =~ s/^[\s\t]*//;
			$value =~ s/[\s\t]*$//;
			$data{$key} = $value;
		}
	}
	close(FILE);
	return %data;
}

sub ErrorPrint {
	my($message) = @_;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "<html>\n";
	print "<head>\n";
	print "<meta http-equiv=\"Content-Language\" content=\"ja\">\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=shift_jis\">\n";
	print "<STYLE TYPE=\"text/css\">\n";
	print "  div	{ font-size: 12px; }\n";
	print "  table	{ font-size: 12px; }\n";
	print "</STYLE>\n";
	print "<center><div>$message</div></center>\n";
	print "</body>\n";
	print "</html>\n";
	exit;
}

sub SetCookie {
	my($CookieName, $CookieValue, $ExpireTime, $Domain, $Path) = @_;
	# URLエンコード
	$CookieValue =~ s/([^\w\=\& ])/'%' . unpack("H2", $1)/eg;
	$CookieValue =~ tr/ /+/;
	my($CookieHeaderString);
	$CookieHeaderString .= "Set-Cookie: $CookieName=$CookieValue\;";
	if($ExpireTime) {
		my(@MonthString) = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
					'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
		my(@WeekString) = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
		my($sec, $min, $hour, $monthday, $month, $year, $weekday) = gmtime($ExpireTime);
		$year += 1900;
		$month = $MonthString[$month];
		if($monthday < 10) {$monthday = '0'.$monthday;}
		if($sec < 10) {$sec = '0'.$sec;}
		if($min < 10) {$min = '0'.$min;}
		if($hour < 10) {$hour = '0'.$hour;}
		my($GmtString) = "$WeekString[$weekday], $monthday-$month-$year $hour:$min:$sec GMT";
 		$CookieHeaderString .= " expires=$GmtString\;";
	}
	if($Domain) {
		$CookieHeaderString .= " domain=$Domain;";
	}
	if($Path) {
		$CookieHeaderString .= " path=$Path;";
	}
	return $CookieHeaderString;
}

sub GetCookie {
	my(@CookieList) = split(/\; /, $ENV{'HTTP_COOKIE'});
	my(%Cookie) = ();
	my($key, $CookieName, $CookieValue);
	for $key (@CookieList) {
		($CookieName, $CookieValue) = split(/=/, $key);
		$CookieValue =~ s/\+/ /g;
		$CookieValue =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C",hex($1))/eg;
		$Cookie{$CookieName} = $CookieValue;
	}
	return %Cookie;
}

sub ClearCookie {
	my($CookieName) = @_;
	my($CookieHeaderString);
	my($ExpiresTimeString) = 'Thu, 01-Jan-1970 00:00:00 GMT';
	$CookieHeaderString .= "Set-Cookie: $CookieName=clear\; expires=$ExpiresTimeString\;";
	return $CookieHeaderString;
}

sub EncryptPasswd {
	my($pass)=@_;
	my(@salt_set)=('a'..'z','A'..'Z','0'..'9','.','/');
	srand;
	my($seed1) = int(rand(64));
	my($seed2) = int(rand(64));
	my($salt) = $salt_set[$seed1] . $salt_set[$seed2];
	return crypt($pass,$salt);
}

sub UnifyReturnCode {
	my($String) = @_;
	$String =~ s/\x0D\x0A/\n/g;
	$String =~ s/\x0D/\n/g;
	$String =~ s/\x0A/\n/g;
	return $String;
}

sub WriteConfData {
	my $err;
	$err .= "<table border=\"0\"><tr><td nowrap>\n";
	$err .= "設定ファイル <tt>$CONF_DATA</tt> をオープンできませんでした。: $!<br>\n";
	$err .= "以下の点をご確認ください。<br>\n";
	$err .= "<ul>\n";
	$err .= "  <li>ディレクトリ <tt>data</tt> のパーミッションを 707 もしくは 777 に変更してみてください。</li>\n";
	$err .= "  <li>ディレクトリ <tt>data</tt> 内の <tt>config.cgi</tt> のパーミッションを 606 もしくは 666 に変更してみてください。</tt>\n";
	$err .= "</ul>\n";
	$err .= "</td></tr></table>\n";
	open(CONF, ">$CONF_DATA") || &ErrorPrint("$err");
	my $key;
	for $key (@CONF_KEYS) {
		print CONF "$key=$CONF{$key}\n";
	}
	close(CONF);
}

sub GetReturnCode {
	my($file) = @_;

	my $size = -s "$file";
	my $str;
	if(open(FILE, "$file")) {
		sysread(FILE, $str, $size);
		close(FILE);
	} else {
		return '';
	}

	my $return_code;
	if($str =~ /\x0D\x0A/) {
		$return_code = 'CRLF';
	} elsif($str =~ /\x0D/) {
		$return_code = 'CR';
	} elsif($str =~ /\x0A/) {
		$return_code = 'LF';
	}
	return $return_code;
}

sub CommaFormat {
	my($num) = @_;
	if($num =~ /[^0-9\.]/) {return $num;}
	my($int, $decimal) = split(/\./, $num);
	my $figure = length $int;
	my $commaformat;
	for(my $i=1;$i<=$figure;$i++) {
		my $n = substr($int, $figure-$i, 1);
		if(($i-1) % 3 == 0 && $i != 1) {
			$commaformat = "$n,$commaformat";
		} else {
			$commaformat = "$n$commaformat";
		}
	}
	if($decimal) {
		$commaformat .= "\.$decimal";
	}
	return $commaformat;
}

sub ReadTemplate {
	my($file) = @_;
	unless(-e $file) {
		&ErrorPrint("テンプレートファイル $file がありません。: $!");
	}
	my $size = -s $file;
	if(!open(FILE, "$file")) {
		&ErrorPrint("テンプレートファイル <tt>$file</tt> をオープンできませんでした。 : $!");
		exit;
	}
	binmode(FILE);
	my $html;
	sysread(FILE, $html, $size);
	close(FILE);
	$html =~ s/\$COPYRIGHT\$/$COPYRIGHT/g;
	return $html;
}

# 連想配列を値（value）でソートした連想配列を返す
sub ValueSort {
	my $x = shift;
	my %array=%$x;
	return sort {$array{$b} <=> $array{$a};} keys %array;
}

sub ConvEpoc2Date {
	my($epoc) = @_;
	my($s, $m, $h, $D, $M, $Y) = localtime($epoc + $CONF{'TIMEDIFF'}*3600);
	$Y += 1900;
	$M += 1;
	$M = sprintf("%02d", $M);
	$D = sprintf("%02d", $D);
	$h = sprintf("%02d", $h);
	$m = sprintf("%02d", $m);
	$s = sprintf("%02d", $s);
	return "$Y/$M/$D $h:$m:$s";
}


