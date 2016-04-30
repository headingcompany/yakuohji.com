#!/usr/bin/perl
################################################################################
# 高機能アクセス解析CGI Professional版 （解析結果表示用）
# Ver 4.7
# Copyright(C) futomi 2001 - 2003
# http://www.futomi.com/
###############################################################################
use strict;
my $JFLAG;
BEGIN {
	use Time::Local;
	use CGI;
	eval "use Jcode";
	if($@) {
		$JFLAG = 0;
	} else {
		$JFLAG = 1;
	}
}
my $q = new CGI;
$| = 1;
require "./jcode.pl";

######################################################################
#  グローバル変数の定義
######################################################################

#バージョン情報
my $CGI_VERSION = '4.7';

#フリーサーバのドメインリスト（正規表現）
my $FREE_SERVER_NAME = '\.tok2\.com|\.infoseek\.co\.jp|\.xrea\.com';

#設定値を取得
my %CONF = &GetConf('./data/config.cgi');
my %URL2PATH = ();
$URL2PATH{$CONF{'URL2PATH_URL'}} = $CONF{'URL2PATH_PATH'};
my @MY_SITE_URLs = split(/,/, $CONF{'MY_SITE_URLs'});
my @REJECT_HOSTS = split(/,/, $CONF{'REJECT_HOSTS'});
my @DIRECTORYINDEX = split(/,/, $CONF{'DIRECTORYINDEX'});

#ディレクトリの定義
my $TEMPLATEDIR = './template';
my $LOGDIR = './logs';
my $PRE_LOGNAME = 'access_log';

#著作権表示の定義
my $COPYRIGHT = "futomi's CGI Cafe - 高機能\アクセス解析CGI Professional $CGI_VERSION";
my $COPYRIGHT2 = "<a href=\"http://www.futomi.com\" target=\"_blank\"><img src=\"$CONF{'IMAGE_URL'}/futomilogo.gif\" width=\"80\" height=\"33\" border=\"0\"></a>";
my $COPYRIGHT3 = "<a href=\"http://www.futomi.com\" target=\"_blank\">futomi's CGI Cafe</a>";
my $COPYRIGHT4 = "<a href=\"http://www.futomi.com\" target=\"_blank\">$COPYRIGHT</a>";

#入力パラメータの取得
my $MODE = $q->param('MODE');
my $ANA_MONTH = $q->param('MONTH');
my $ANA_DAY = $q->param('DAY');
my $TARGET_FRAME = $q->param('FRAME');
my $ITEM = $q->param('ITEM');
my $TARGET_VISITOR = $q->param('VISITOR');

# このCGIのURL
my $CGI_URL = 'acc.cgi';

# 解析対象のログファイル名を特定
my $TARGET_LOGNAME = &SpecifyLogFileName;

######################################################################
#  メインルーチン
######################################################################

# パスワード認証
if($CONF{'AUTHFLAG'}) {&Auth;}

# リクエストにredirectキーワードがあれば、指定URLへ転送
if($q->param('REDIRECT')) {
	&RedirectPage($q->param('REDIRECT'));
}

# ターゲットフレームの指定がなければ、親フレームを出力する。
if($TARGET_FRAME eq 'menu') {
	&PrintMenuFrame;
} elsif($TARGET_FRAME eq 'result') {
	&PrintResultFrame;
} else {
	&PrintMainFrame;
}

exit;


######################################################################
#  サブルーチン
######################################################################

sub PrintMainFrame {
	my $menu_url = "$CGI_URL?FRAME=menu";
	my $result_url = "$CGI_URL?FRAME=result";
	if($TARGET_LOGNAME) {
		$menu_url .= "\&LOG=$TARGET_LOGNAME";
		$result_url .= "\&LOG=$TARGET_LOGNAME";
	}
	if($ANA_MONTH) {
		$menu_url .= "\&MONTH=$ANA_MONTH";
		$result_url .= "\&MONTH=$ANA_MONTH";
		if($ANA_DAY) {
			$menu_url .= "\&DAY=$ANA_DAY";
			$result_url .= "\&DAY=$ANA_DAY";
		}
	} else {
		if($ANA_DAY) {
			&ErrorPrint("日を指定する場合には、月を指定して下さい。");
		}
	}
	my $html = &ReadTemplate("$TEMPLATEDIR/mainframe.html");
	$html =~ s/<!--MENUURL-->/$menu_url/;
	$html =~ s/<!--RESULTURL-->/$result_url/;
	if($ENV{'SERVER_NAME'} =~ /($FREE_SERVER_NAME)/) {
		$html =~ s/<!--COOKIE-->/<META HTTP-EQUIV='Set-Cookie' CONTENT=PASS=$CONF{'PASSWORD'};'>/;
	} else {
		$html =~ s/<!--COOKIE-->//;
	}
	&HtmlHeader;
	print "$html\n";
}

sub PrintMenuFrame {
	my(@DateList) = &GetLogDateList("$LOGDIR/$TARGET_LOGNAME");
	my $Today = &GetToday;
	my $MaxDate = pop @DateList;
	my $MinDate = $MaxDate;
	if(scalar(@DateList) >= 1) {
		$MinDate = shift @DateList;
	}

	my $TargetMonth;
	if($ANA_MONTH) {
		$TargetMonth = $ANA_MONTH;
	} elsif($MaxDate) {
		$TargetMonth = substr($MaxDate, 0, 6);
	} else {
		$TargetMonth = substr($Today, 0, 6);
	}

	my $DspYear = substr($TargetMonth, 0, 4);
	my $DspMonth = substr($TargetMonth, 4, 2);
	my $y = $DspYear;	$y =~ s/^0//;
	my $m = $DspMonth;	$m =~ s/^0//;
	my $LastMonth = &GetLastMonth($TargetMonth);
	my $NextMonth = &GetNextMonth($TargetMonth);
	
	my $ThisMonthTag = "<a href=\"$CGI_URL?LOG=$TARGET_LOGNAME&MONTH=$DspYear$DspMonth\" target=\"_top\">$DspYear年 $DspMonth月</a>";
	my $LastMonthTag;
	if($LastMonth >= substr($MinDate, 0, 6)) {
		$LastMonthTag = "<a href=\"$CGI_URL?LOG=$TARGET_LOGNAME&MONTH=$LastMonth\" target=\"_top\"><img src=\"$CONF{'IMAGE_URL'}/left.gif\" border=\"0\" width=\"17\" height=\"17\"></a>\n";
	} else {
		$LastMonthTag = "<img src=\"$CONF{'IMAGE_URL'}/left_g.gif\" border=\"0\" width=\"17\" height=\"17\">\n";
	}
	my $NextMonthTag;
	if($NextMonth <= substr($MaxDate, 0, 6)) {
		$NextMonthTag = "<a href=\"$CGI_URL?LOG=$TARGET_LOGNAME&MONTH=$NextMonth\" target=\"_top\"><img src=\"$CONF{'IMAGE_URL'}/right.gif\" border=\"0\" width=\"17\" height=\"17\"></a>\n";
	} else {
		$NextMonthTag = "<img src=\"$CONF{'IMAGE_URL'}/right_g.gif\" border=\"0\" width=\"17\" height=\"17\">\n";
	}

	my $LastDay = &LastDay($DspYear, $DspMonth);
	my $StartWeekNo = &Youbi($DspYear, $DspMonth, "01");
	my $flag = 1;
	my $WeekNo = 0;
	my $day = 1;
	my ($i, $DateBuff, $DspDay, $CalendarTag);
	while($flag) {
		$CalendarTag .= "<tr>\n";
		for($i=0;$i<7;$i++) {
			if($WeekNo < 1 && $i < $StartWeekNo) {
				$CalendarTag .= "  <td align=\"right\" bgcolor=\"#EAEAEA\">&nbsp;</td>\n";
			} elsif($day > $LastDay) {
				$CalendarTag .= "  <td align=\"right\" bgcolor=\"#EAEAEA\">&nbsp;</td>\n";
				$day ++;
			} else {
				$DateBuff = $DspYear . $DspMonth;
				if($day < 10) {
					$DateBuff .= "0$day";
				} else {
					$DateBuff .= "$day";
				}
				if($DateBuff == $Today) {
					$DspDay = "<strong>$day</strong>";
				} else {
					$DspDay = "$day";
				}
				if($i == 0) {
					$DspDay = "<font color=\"#FF0000\">$DspDay</font>";
				} elsif(&CheckHoliday($y, $m, $day)) {
					$DspDay = "<font color=\"#FF0000\">$DspDay</font>";
				} elsif($i == 6) {
					$DspDay = "<font color=\"#0000FF\">$DspDay</font>";
				}
				if($DateBuff >= $MinDate && $DateBuff <= $MaxDate) {
					$CalendarTag .= "  <td align=\"right\" bgcolor=\"\#FFFFCC\"><a href=\"$CGI_URL?LOG=$TARGET_LOGNAME&MONTH=$DspYear$DspMonth&DAY=$day\" target=\"_top\">$DspDay</a></td>\n";
				} else {
					$CalendarTag .= "  <td align=\"right\">$DspDay</td>\n";
				}
				$day ++;
			}
		}
		$CalendarTag .= "</tr>\n";
		$WeekNo ++;
		if($day > $LastDay) {
			$flag = 0;
		}
	}

	my $LogListTag = "<form action=\"$CGI_URL\" method=\"POST\" target=\"_top\">\n";
	$LogListTag .= "  <select size=\"1\" name=\"LOG\">\n";
	opendir(LOGDIR, "$LOGDIR") || &ErrorPrint("ログ格納ディレクトリ「$LOGDIR」をオープンできませんでした。 : $!");
	my @files = readdir(LOGDIR);
	closedir(LOGDIR);
	for my $file (sort @files) {
		if($file =~ /^$PRE_LOGNAME/) {
			if($file eq $TARGET_LOGNAME) {
				$LogListTag .= "    <option value=\"$file\" selected>$file</option>\n";
			} else {
				$LogListTag .= "    <option value=\"$file\">$file</option>\n";
			}
		}
	}
	$LogListTag .= "  </select><br>\n";
	$LogListTag .= "  <input type=\"submit\" name=\"LOGSELECT\" value=\"ログ切替\">\n";
	$LogListTag .= "</form>\n";


	my $AccModeTag;
	if($ANA_DAY) {
		$AccModeTag = "日指定<br>".substr($ANA_MONTH, 0, 4)."/".substr($ANA_MONTH, 4, 2)."/$ANA_DAY";
	} elsif($ANA_MONTH) {
		$AccModeTag = "月指定<br>".substr($ANA_MONTH, 0, 4)."/".substr($ANA_MONTH, 4, 2);
	} else {
		$AccModeTag = "全指定";
	}

	my $CgiUrl = "$CGI_URL\?FRAME=result\&LOG=$TARGET_LOGNAME";
	if($ANA_MONTH) {
		$CgiUrl .= "&MONTH=$ANA_MONTH";
		if($ANA_DAY) {
			$CgiUrl .= "&DAY=$ANA_DAY";
		}
	}

	my $AllAccUrl = "$CGI_URL\?LOG=$TARGET_LOGNAME";

	my $template;
	if($ENV{'HTTP_USER_AGENT'} =~ /Opera/i) {
		$template = "$TEMPLATEDIR/menuframe.html";
	}elsif($ENV{'HTTP_USER_AGENT'} =~ /MSIE/i) {
		$template = "$TEMPLATEDIR/menuframe_ie.html";
	} else {
		$template = "$TEMPLATEDIR/menuframe.html";
	}
	my $html = &ReadTemplate($template);
	$html =~ s/<!--LastMonth-->/$LastMonthTag/;
	$html =~ s/<!--ThisMonth-->/$ThisMonthTag/;
	$html =~ s/<!--NextMonth-->/$NextMonthTag/;
	$html =~ s/<!--ALLACCURL-->/$AllAccUrl/;
	$html =~ s/<!--calendar-->/$CalendarTag/;
	$html =~ s/<!--loglist-->/$LogListTag/;
	$html =~ s/<!--ACCMODE-->/$AccModeTag/;
	$html =~ s/<!--MYURL-->/$CGI_URL/;
	$html =~ s/<!--CGIURL-->/$CgiUrl/g;
	$html =~ s/<!--IMAGEDIR-->/$CONF{'IMAGE_URL'}/g;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
}

sub IsInDate {
	my($date_check) = @_;
	my($date_check_mon, $date_check_day) = $date_check =~ /^(\d{6})(\d{2})/;
	$date_check_day =~ s/^0//;
	if($ANA_MONTH) {
		unless($date_check_mon eq $ANA_MONTH) {
			return 0;
		}
		if($ANA_DAY) {
			unless($date_check_day eq $ANA_DAY) {
				return 0;
			}
		}
	}
	return 1;
}

sub PrintResultFrame {
	if($ITEM eq '') {
		&GeneralStatistics;
	} elsif($ITEM eq 'AccessLogInformation') {
		&AccessLogInformation;
	} elsif($ITEM eq 'LogSearch') {
		&LogSearchForm;
	} elsif($ITEM eq 'LogSearchGo') {
		&LogSearchGo;
	} elsif($ITEM eq 'TopVisitors') {
		&TopVisitors;
	} elsif($ITEM eq 'MostActiveCountries') {
		&MostActiveCountries;
	} elsif($ITEM eq 'MostActivePrefecture') {
		&MostActivePrefecture;
	} elsif($ITEM eq 'MostActiveOrganization') {
		&MostActiveOrganization;
	} elsif($ITEM eq 'NewVsReturningVisitors') {
		&NewVsReturningVisitors;
	} elsif($ITEM eq 'TopPagesByViews') {
		&TopPagesByViews;
	} elsif($ITEM eq 'TopPagesByVisits') {
		&TopPagesByVisits;
	} elsif($ITEM eq 'TopPagesByVisitors') {
		&TopPagesByVisitors;
	} elsif($ITEM eq 'VisitorTrace') {
		&VisitorTrace;
	} elsif($ITEM eq 'ActivityByDayOfTheMonth') {
		&ActivityByDayOfTheMonth;
	} elsif($ITEM eq 'ActivityByDayOfTheWeek') {
		&ActivityByDayOfTheWeek;
	} elsif($ITEM eq 'ActivityByHourOfTheDay') {
		&ActivityByHourOfTheDay;
	} elsif($ITEM eq 'TopReferringSites') {
		&TopReferringSites;
	} elsif($ITEM eq 'TopReferringURLs') {
		&TopReferringURLs;
	} elsif($ITEM eq 'TopSearchKeywords') {
		&TopSearchKeywords;
	} elsif($ITEM eq 'TopSearchEngines') {
		&TopSearchEngines;
	} elsif($ITEM eq 'TopBrowsers') {
		&TopBrowsers;
	} elsif($ITEM eq 'TopPlatforms') {
		&TopPlatforms;
	} elsif($ITEM eq 'TopAcceptLanguage') {
		&TopAcceptLanguage;
	} elsif($ITEM eq 'TopResolution') {
		&TopResolution;
	} elsif($ITEM eq 'TopColorDepth') {
		&TopColorDepth;
	} elsif($ITEM eq 'TopVideoMemorySize') {
		&TopVideoMemorySize;
	} else {
		&ErrorPrint("不正なリクエストです。");
	}
}

sub GeneralStatistics {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my $min_date = 99999999999999;
	my $max_date = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		$max_date = $date_part;
		if($i == 0) {$min_date = $date_part;}
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);
	my $PageViewNum = $i;

	# 総セッション数を調べる
	my $AllSessionNum = &GetSessionNum(\@LogNoList, \%date, \%remote_host, \%cookies);
	# 総ユニークユーザー数を調べる。
	my $AllUniqueUserNum = &GetUniqueUserNum(\@LogNoList, \%remote_host, \%cookies);
	my $PVperUser = sprintf("%.2f", $PageViewNum / $AllUniqueUserNum);
	# 今日のログ番号を取得する
	my $Today = &GetToday;
	my @TodayLogNoList = ();
	for my $i (keys %date) {
		if($date{$i} =~ /^$Today/) {
			push(@TodayLogNoList, $i);
		}
	}
	my $TodayPV = @TodayLogNoList;
	my $TodaySessionNum = &GetSessionNum(\@TodayLogNoList, \%date, \%remote_host, \%cookies);
	my $TodayUniqueUserNum = &GetUniqueUserNum(\@TodayLogNoList, \%remote_host, \%cookies);
	my $TodayPVperUser;
	if($TodayUniqueUserNum > 0) {
		$TodayPVperUser = sprintf("%.2f", $TodayPV / $TodayUniqueUserNum);
	} else {
		$TodayPVperUser = 0;
	}
	my($min_year, $min_mon, $min_mday, $min_hour, $min_min, $min_sec) = $min_date =~ /^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/;
	my($max_year, $max_mon, $max_mday, $max_hour, $max_min, $max_sec) = $max_date =~ /^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/;
	my @Keys = (
		'解析対象期間',
		'ページビュー',
		'セッション数',
		'ユニークユーザー数',
		'一人あたりのページビュー'
	);
	my %Data = (
		'解析対象期間' => "$min_year/$min_mon/$min_mday $min_hour:$min_min:$min_sec ～ $max_year/$max_mon/$max_mday $max_hour:$max_min:$max_sec",
		'ページビュー' => $PageViewNum,
		'セッション数' => $AllSessionNum,
		'ユニークユーザー数' => $AllUniqueUserNum,
		'一人あたりのページビュー' => $PVperUser
	);
	my $Str;
	$Str .= &MakeTable(\@Keys, \%Data);
	$Str .= "<hr>\n";
	$Str .= "<div>本日のアクセス状況</div><br>\n";
	@Keys = (
		'ページビュー',
		'セッション数',
		'ユニークユーザー数',
		'一人あたりのページビュー'
	);
	%Data = (
		'ページビュー' => $TodayPV,
		'セッション数' => $TodaySessionNum,
		'ユニークユーザー数' => $TodayUniqueUserNum,
		'一人あたりのページビュー' => $TodayPVperUser
	);
	$Str .= &MakeTable(\@Keys, \%Data);
	my $Title = '統計概要';
	&PrintResult($Title, $Str);
}


sub AccessLogInformation {
	# 過去ログリストを取得する
	my %LogList = ();
	unless($LOGDIR) {$LOGDIR = '.';}
	opendir(LOGDIR, "$LOGDIR") || &ErrorPrint("ログ格納ディレクトリ「$LOGDIR」をオープンできませんでした。");
	my @log_namaes = readdir(LOGDIR);
	closedir(LOGDIR);
	my($key);
	for $key (@log_namaes) {
		if($key =~ /^$PRE_LOGNAME/) {
			$LogList{$key} = "$LOGDIR\/$key";
		}
	}

	my($Str);
	$Str .= "<form action=\"$CGI_URL\" method=\"POST\" target=\"_top\">\n";
	# ログファイル欄
	my($LogListStr);
	$LogListStr .= "<select name=\"LOG\">\n";;
	for $key (sort(keys(%LogList))) {
		if($key eq $TARGET_LOGNAME) {
			$LogListStr .= "<option value=\"$key\" selected>$key</option>\n";
		} else {
			$LogListStr .= "<option value=\"$key\">$key</option>\n";
		}
	}
	$LogListStr .= "</select>\n";
	$LogListStr .= "<input type=\"submit\" VALUE=\"ログ切替\" NAME=\"LOGSELECT\">\n";


	# ログファイルサイズ欄
	my $LogSize = &AnalyzeLogfileSize("$LOGDIR/$TARGET_LOGNAME");
	my $LogSizeStr = &CommaFormat($LogSize);
	$LogSizeStr .= " バイト";

	# ログローテーションサイズ欄
	my $LogLotationStr;
	if($CONF{'LOTATION'} eq '0' || $CONF{'LOTATION'} eq '') {
		$LogLotationStr = 'ローテーションしない';
	} elsif($CONF{'LOTATION'} eq '1') {
		my $LogSizeRate = int($LogSize * 1000 / $CONF{'LOTATION_SIZE'}) / 10;
		if($LogSizeRate > 100) {$LogSizeRate = 100;}
		my $LogSizeGraphMaxLen = 150;	#ピクセル
		my $LogSizeGraphLen = int($LogSizeGraphMaxLen * $LogSizeRate / 100);	#ピクセル
		my $dsp_lotation_size = &CommaFormat($CONF{'LOTATION_SIZE'});
		$LogLotationStr .= "$dsp_lotation_size byte でローテーション<br>\n";
		$LogLotationStr .= "（使用率 $LogSizeRate%）\n";
		$LogLotationStr .= "<table border=\"0\" width=\"$LogSizeGraphMaxLen\" cellpadding=\"0\"><tr><td CLASS=ListHeader2 align=\"left\">\n";
		$LogLotationStr .= "<table border=\"0\" width=\"$LogSizeGraphLen\" cellpadding=\"0\"><tr><td CLASS=ListHeader3>&nbsp;</td></tr></table>\n";
		$LogLotationStr .= "</td></tr></table>\n";

		# 対象ログの調査開始時と調査終了時を調べる
		if(-e "$LOGDIR/$TARGET_LOGNAME") {
			open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
		} else {
			&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
		}
		my $min_date = 99999999999999;
		my $max_date = 0;
		my $i = 0;
		while(<LOGFILE>) {
			chop;
			my($date_part);
			if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
				$date_part = $1;
			} else {
				next;
			}
			next if($date_part eq '');
			next unless(&IsInDate($date_part));
			$max_date = $date_part;
			if($i == 0) {$min_date = $date_part;}
			$i ++;
		}
		close(LOGFILE);

		my $RangeSec = &GetRangeSecond($min_date, $max_date);	# 期間を秒に変換
		my $RemainSec = int( ($CONF{'LOTATION_SIZE'} - $LogSize) * $RangeSec / $LogSize );
		my @DateParts = localtime(time + $CONF{'TIMEDIFF'}*60*60 + $RemainSec);
		$DateParts[5] += 1900;
		$DateParts[4] ++;
		for (my $i=0;$i<=5;$i++) {
			if($DateParts[$i] < 10) {$DateParts[$i] = "0$DateParts[$i]";}
		}
		my $DispRemainSec = &CommaFormat($RemainSec);
		$LogLotationStr .= "ローテーション推定日時<br>\n";
		$LogLotationStr .= "$DateParts[5]年$DateParts[4]月$DateParts[3]日 $DateParts[2]:$DateParts[1]:$DateParts[0] （あと $DispRemainSec 秒）";
	} elsif($CONF{'LOTATION'} eq '2') {
		$LogLotationStr = '日ごとにローテーション';
	} elsif($CONF{'LOTATION'} eq '3') {
		$LogLotationStr = '月ごとにローテーション';
	} elsif($CONF{'LOTATION'} eq '4') {
		$LogLotationStr = '週ごとにローテーション';
	}

	#ログ一覧
	my(%size_list, %mtime_list);
	for my $file (sort keys %LogList) {
		my @stat = stat("$LOGDIR/$file");
		$size_list{$file} = $stat[7];
		$mtime_list{$file} = $stat[9];
	}
	my $LogAllListStr;
	foreach my $file (ValueSort(\%mtime_list)) {
		my $date = &ConvEpoc2Date($mtime_list{$file});
		my $dsp_size = &CommaFormat($size_list{$file});
		$LogAllListStr .= "  <tr>\n";
		$LogAllListStr .= "    <td class=\"ListHeader4\">$file</td>\n";	#ファイル名
		$LogAllListStr .= "    <td class=\"ListHeader4\" align=\"right\">$dsp_size byte</td>\n";	#サイズ
		$LogAllListStr .= "    <td class=\"ListHeader4\">$date</td>\n";	#最終更新日時
		if($file eq $TARGET_LOGNAME) {
			$LogAllListStr .= "    <td class=\"ListHeader4\" align=\"center\">選択中</td>\n";		#ログ切替
		} else {
			$LogAllListStr .= "    <td class=\"ListHeader4\" align=\"center\"><a href=\"$CGI_URL?LOG=$file\" target=\"_top\">解析</a></td>\n";		#ログ切替
		}
		$LogAllListStr .= "  </tr>\n";
	}

	my $html = &ReadTemplate("./template/loginfo.html");
	$html =~ s/\$CGIURL\$/$CGI_URL/;
	$html =~ s/\$LOGFILE\$/$LogListStr/;
	$html =~ s/\$LOGSIZE\$/$LogSizeStr/;
	$html =~ s/\$LOGLOTATION\$/$LogLotationStr/;
	$html =~ s/\$LOGALLLIST\$/$LogAllListStr/;
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	print "$html\n";
	exit;
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

sub LogSearchForm {
	my $html = &ReadTemplate("$TEMPLATEDIR/search.html");
	my $log = $q->param('LOG');
	my $hidden;
	$hidden .= "<input type=\"hidden\" name=\"LOG\" value=\"$log\">\n";
	$hidden .= "<input type=\"hidden\" name=\"ITEM\" value=\"LogSearchGo\">\n";
	$hidden .= "<input type=\"hidden\" name=\"FRAME\" value=\"result\">\n";
	$html =~ s/\$CGI_URL\$/$CGI_URL/;
	$html =~ s/\$HIDDEN\$/$hidden/;
	$html =~ s/\$MODE1\$/checked/;
	$html =~ s/\$MODE2\$//;
	$html =~ s/\$DATE0\$/checked/;
	$html =~ s/\$DATE1\$//;
	$html =~ s/\$(S|E)(YEAR|MON|DAY)\$//g;
	$html =~ s/\$QSTRING\$//;
	$html =~ s/\$DISPNUM\$/20/;
	$html =~ s/\$HITNUM\$//g;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
	exit;
}

sub  LogSearchGo {
	my $mode = $q->param('MODE');
	my $date_opt = $q->param('DATE');
	my $syear = $q->param('SYEAR');
	my $eyear = $q->param('EYEAR');
	my $smon = $q->param('SMON');
	my $emon = $q->param('EMON');
	my $sday = $q->param('SDAY');
	my $eday = $q->param('EDAY');
	my $qstring = $q->param('QSTRING');
	my $dispnum = $q->param('DISPNUM');
	my $next = $q->param('NEXT');
	unless($next) {$next = 1;}
	if($mode eq '') {
		$mode = '1';
	} elsif($mode !~ /^(1|2)$/) {
		&ErrorPrint("不正なアクセスです。");
	}
	if($date_opt) {
		unless($syear && $smon && $sday) {
			&ErrorPrint("日付を指定して下さい。");
		}
	}
	my @date_nums = ($syear, $smon, $sday, $eyear, $emon, $eday);
	my @conv = ();
	for my $num (@date_nums) {
		&jcode::tr(\$num, '０-９', '0-9');
		if($num =~ /[^0-9]/) {
			&ErrorPrint("日付は数字で指定して下さい。");
		}
		$num =~ s/^0+//;
		if($num eq '') {$num = "0";}
		if($num < 10) {$num = "0$num";}
		push(@conv, $num);
	}
	my $start = "$conv[0]$conv[1]$conv[2]";
	my $end = "$conv[3]$conv[4]$conv[5]";
	&jcode::tr(\$dispnum, '０-９', '0-9');
	if($dispnum =~ /[^0-9]/) {
		&ErrorPrint("表示件数は数字で指定して下さい。");
	}
	unless($dispnum) {$dispnum = 100;}
	if($next eq '') {$next = 0;}
	if($date_opt) {$end = $start;}
	if($start > $end) {
		&ErrorPrint("検索開始日は、検索終了日より前の日を指定して下さい。");
	}
	my $qstring_secure = &SecureHtml($qstring);
	$qstring =~ s/([\+\.\[\]\(\)\$\@\?\\\-\^\|\*\{\}\/])/\\$1/g;
	$qstring =~ s/\s+/ /g;
	$qstring =~ s/^\s//;
	$qstring =~ s/\s$//;
	my @q_parts = split(/\s/, $qstring);
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my @search_list = ();
	my $hitnum = 0;

	if($mode eq '1') {
		#直近のログだけを検索表示する
		while(<LOGFILE>) {
			chop;
			my $line = $_;
			if($date_opt) {
				$line =~ m/^(\S+)\s/;
				my $access_date = $1;
				$access_date = substr($access_date, 0, 8);
				unless($access_date >= $start && $access_date <= $end) {next;}
			}
			my $q_flag = 1;
			if(@q_parts) {
				for my $key (@q_parts) {
					unless($line =~ /$key/i) {
						$q_flag = 0;
					}
				}
			}
			unless($q_flag) {next;}
			$hitnum ++;
			my $array_num = scalar @search_list;
			if($array_num >= $dispnum) {
				shift @search_list;
			}
			push(@search_list, $line);
		}
		close(LOGFILE);
	} else {
		#ログの先頭から順次検索表示する
		while(<LOGFILE>) {
			chop;
			my $line = $_;
			if($date_opt) {
				$line =~ m/^(\S+)\s/;
				my $access_date = $1;
				$access_date = substr($access_date, 0, 8);
				unless($access_date >= $start && $access_date <= $end) {next;}
			}
			my $q_flag = 1;
			if(@q_parts) {
				for my $key (@q_parts) {
					unless($line =~ /$key/i) {
						$q_flag = 0;
					}
				}
			}
			unless($q_flag) {next;}
			$hitnum ++;
			if($hitnum < $next) {next;}
			my $array_num = scalar @search_list;
			if($array_num >= $dispnum) {
				next;
			}
			push(@search_list, $line);
		}
		close(LOGFILE);
	}
	my $html_all = &ReadTemplate("$TEMPLATEDIR/search.html");
	my($html) = split(/<!-- delimiter -->/, $html_all);
	my $log = $q->param('LOG');
	my $hidden;
	$hidden .= "<input type=\"hidden\" name=\"LOG\" value=\"$log\">\n";
	$hidden .= "<input type=\"hidden\" name=\"ITEM\" value=\"LogSearchGo\">\n";
	$hidden .= "<input type=\"hidden\" name=\"FRAME\" value=\"result\">\n";
	$html =~ s/\$CGI_URL\$/$CGI_URL/;
	$html =~ s/\$HIDDEN\$/$hidden/;
	$html =~ s/\$MODE$mode\$/checked/;
	$html =~ s/\$MODE[0-9]+$//g;
	$html =~ s/\$DATE$date_opt\$/checked/;
	$html =~ s/\$DATE[0-9]+$//g;
	$html =~ s/\$SYEAR\$/$syear/;
	$html =~ s/\$EYEAR\$/$eyear/;
	$html =~ s/\$SMON\$/$smon/;
	$html =~ s/\$EMON\$/$emon/;
	$html =~ s/\$SDAY\$/$sday/;
	$html =~ s/\$EDAY\$/$eday/;
	$html =~ s/\$DISPNUM\$/$dispnum/;
	$html =~ s/\$QSTRING\$/$qstring_secure/;
	$html =~ s/\$HITNUM\$/検索件数 ：$hitnum 件/g;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
	my $n;
	if($mode eq '1') {
		$n = $hitnum - $dispnum + 1;
	} else {
		$n = $next;
	}
	for my $line (@search_list) {
		&jcode::convert(\$line, 'sjis');
		$line = &SecureHtml($line);
		if($n % 2) {
			print "<div class=\"style1\">";
		} else {
			print "<div class=\"style2\">";
		}
		print "<b>$n :</b> <tt>$line</tt>";
		print "</div>\n";
		$n ++;
	}
	if($mode eq '2') {
		print "<HR>\n";
		my $next_tag_num = $n;
		my $prev_tag_num = $next - $dispnum;
		print "<table border=\"0\" width=\"100%\"><tr>\n";
		print "  <td align=\"left\">";
		if($prev_tag_num > 0) {
			#前へを表示
			print "<a href=\"$CGI_URL\?LOG=$log&ITEM=LogSearchGo&FRAME=result&MODE=$mode&DATE=$date_opt&SYEAR=$syear&EYEAR=$eyear&SMON=$smon&EMON=$emon&SDAY=$sday&EDAY=$eday&QSTRING=$qstring_secure&DISPNUM=$dispnum&NEXT=$prev_tag_num\">&lt;&lt;前へ</a>\n";
		}
		print "  </td>\n";
		print "  <td align=\"right\">";
		if($next_tag_num <= $hitnum) {
			#次へを表示
			print "<a href=\"$CGI_URL\?LOG=$log&ITEM=LogSearchGo&FRAME=result&MODE=$mode&DATE=$date_opt&SYEAR=$syear&EYEAR=$eyear&SMON=$smon&EMON=$emon&SDAY=$sday&EDAY=$eday&QSTRING=$qstring_secure&DISPNUM=$dispnum&NEXT=$next_tag_num\">次へ&gt;&gt;</a>\n";
		}
		print "  </td>\n";
		print "</tr></table>\n";
	}

	print "</BODY></HTML>\n";
	exit;
}

sub TopVisitors {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %HostLogNoList = ();	
	for my $i (keys(%remote_host)) {
		$HostLogNoList{$remote_host{$i}} .= "$i,";
	}
	my($HostName, @NoList, $Views, $Sessions, $KeyStr);
	my %SessionNumList = ();
	my %PageViewNumList = ();
	for $HostName (keys(%HostLogNoList)) {
		$KeyStr = "<a href=\"$CGI_URL?FRAME=result&ITEM=VisitorTrace&LOG=$TARGET_LOGNAME&VISITOR=$HostName";
		if($ANA_MONTH) {
			$KeyStr .= "&MONTH=$ANA_MONTH";
			if($ANA_DAY) {
				$KeyStr .= "&DAY=$ANA_DAY";
			}
		}
		$KeyStr .= "\">";
		$KeyStr .= "$HostName";
		$KeyStr .= "</a>";
		$HostLogNoList{$HostName} =~ s/,$//;
		@NoList = split(/,/, $HostLogNoList{$HostName});
		$Views = @NoList;
		$PageViewNumList{$KeyStr} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$KeyStr} = $Sessions;
	}
	my($Str);
	$Str .= "ページビュー<br>\n";
	my @Titles = ('順位', 'アクセス元ホスト名', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph(\%PageViewNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	@Titles = ('順位', 'アクセス元ホスト名', '訪問数', 'グラフ');
	$Str .= &MakeGraph(\%SessionNumList, \@Titles);
	my $Title = 'アクセス元ホスト名ランキング';
	&PrintResult($Title, $Str);
}


sub MostActiveCountries {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %CountryLogNoList = ();
	my %IpList = &ReadIpList;
	for my $i (keys %remote_host) {
		my $domain;
		if($remote_host{$i} =~ /[^0-9\.]/) {
			$domain = $remote_host{$i};
		} else {
			$domain = &GetDomainByAddr($remote_host{$i}, \%IpList);
		}
		if($domain) {
			my @parts = split(/\./, $domain);
			my $tl = pop @parts;
			$tl = lc $tl;
		  	$CountryLogNoList{$tl} .= "$i,";
		} else {
			$CountryLogNoList{'?'} .= "$i,";
		}
	}
	my(@NoList, $Views, $Sessions, $Unique);
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	my $tld;
	for $tld (keys %CountryLogNoList) {
		$CountryLogNoList{$tld} =~ s/,$//;
		@NoList = split(/,/, $CountryLogNoList{$tld});
		$Views = @NoList;
		$PageViewNumList{$tld} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$tld} = $Sessions;
		$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$tld} = $Unique;
	}
	my $Str;
	my %TldList = &ReadDef('./data/country_code.dat');
	$Str .= "ページビュー<br>\n";
	$Str .= &MakeCircleGraph(\%PageViewNumList);
	$Str .= "<br>\n";
	my @Titles = ('順位', 'TLD', '国名', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph2(\%PageViewNumList, \@Titles, \%TldList);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	$Str .= &MakeCircleGraph(\%SessionNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', 'TLD', '国名', '訪問数', 'グラフ');
	$Str .= &MakeGraph2(\%SessionNumList, \@Titles, \%TldList);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	$Str .= &MakeCircleGraph(\%UniqueNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', 'TLD', '国名', '訪問者数', 'グラフ');
	$Str .= &MakeGraph2(\%UniqueNumList, \@Titles, \%TldList);
	my $Title = 'アクセス元国名（TLD）ランキング';
	&PrintResult($Title, $Str);
}


sub MostActivePrefecture {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %OrgList = &ReadDef('./data/organization.dat');
	my %PrefList = &ReadDef('./data/pref.dat');
	my %IpList = &ReadIpList;

	my %PrefLogNoList = ();
	my($Str1, $Str2, $GetPref);
	for my $i (keys %remote_host) {
		$GetPref = '';
		my $host = lc $remote_host{$i};
		if($host =~ /[^0-9\.]/) {
			my $PrefKeyword = &GetPrefKeyword($host);
			if($PrefKeyword) {
				$GetPref = $PrefList{$PrefKeyword};
			} else {
				$host =~ m/([\w\-]+\.[\w\-]+\.[\w\-]+)$/;
				my $domain = $1;
				($Str1, $Str2, $GetPref) = split(/,/, $OrgList{$domain});
				unless($GetPref) {
					$host =~ m/([\w\-]+\.[\w\-]+)$/;
					($Str1, $Str2, $GetPref) = split(/,/, $OrgList{$domain});
				}
			}
			unless($GetPref) {next;}
			$PrefLogNoList{$GetPref} .= "$i,";
		} else {
			my $domain = &GetDomainByAddr($host, \%IpList);
			($Str1, $Str2, $GetPref) = split(/,/, $OrgList{$domain});
			$PrefLogNoList{$GetPref} .= "$i,";
		}
	}
	my($Pref, @NoList, $Views, $Sessions, $Unique);
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for $Pref (keys %PrefLogNoList) {
		$PrefLogNoList{$Pref} =~ s/,$//;
		@NoList = split(/,/, $PrefLogNoList{$Pref});
		$Views = @NoList;
		$PageViewNumList{$Pref} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$Pref} = $Sessions;
		$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$Pref} = $Unique;
	}
	my $Str = '';
	$Str .= "ページビュー<br>\n";
	$Str .= &MakeCircleGraph(\%PageViewNumList);
	$Str .= "<br>\n";
	my @Titles = ('順位', '都道府県名', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph(\%PageViewNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	$Str .= &MakeCircleGraph(\%SessionNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '都道府県名', '訪問数', 'グラフ');
	$Str .= &MakeGraph(\%SessionNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	$Str .= &MakeCircleGraph(\%UniqueNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '都道府県名', '訪問者数', 'グラフ');
	$Str .= &MakeGraph(\%UniqueNumList, \@Titles);
	my $Title = 'アクセス元都道府県ランキング';
	&PrintResult($Title, $Str);
}


sub MostActiveOrganization {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %tld_fix = (
		'com' =>'2', 'net'=>'2', 'org'=>'2', 'biz'=>'2', 'info'=>'2', 'name'=>'3',
		'aero'=>'2', 'coop'=>'2', 'museum'=>'2', 'pro'=>'3', 'edu'=>'2', 'gov'=>'2',
		'mil'=>'2', 'int'=>'2', 'arpa'=>'2', 'nato'=>'2',
		'hk'=>'3', 'sg'=>'3', 'kr'=>'3', 'uk'=>'3'
	);
	my %sld_fix = (
		#日本
		'ac.jp'=>'3', 'ad.jp'=>'3', 'co.jp'=>'3', 'ed.jp'=>'3', 'go.jp'=>'3',
		'gr.jp'=>'3', 'lg.jp'=>'3', 'ne.jp'=>'3', 'or.jp'=>'3',
		'hokkaido.jp'=>'3', 'aomori.jp'=>'3', 'iwate.jp'=>'3', 'miyagi.jp'=>'3',
		'akita.jp'=>'3', 'yamagata.jp'=>'3', 'fukushima.jp'=>'3', 'ibaraki.jp'=>'3',
		'tochigi.jp'=>'3', 'gunma.jp'=>'3', 'saitama.jp'=>'3', 'chiba.jp'=>'3',
		'tokyo.jp'=>'3', 'kanagawa.jp'=>'3', 'niigata.jp'=>'3', 'toyama.jp'=>'3',
		'ishikawa.jp'=>'3', 'fukui.jp'=>'3', 'yamanashi.jp'=>'3', 'nagano.jp'=>'3',
		'gifu.jp'=>'3', 'shizuoka.jp'=>'3', 'aichi.jp'=>'3', 'mie.jp'=>'3',
		'shiga.jp'=>'3', 'kyoto.jp'=>'3', 'osaka.jp'=>'3', 'hyogo.jp'=>'3',
		'nara.jp'=>'3', 'wakayama.jp'=>'3', 'tottori.jp'=>'3', 'shimane.jp'=>'3',
		'okayama.jp'=>'3', 'hiroshima.jp'=>'3', 'yamaguchi.jp'=>'3', 'tokushima.jp'=>'3',
		'kagawa.jp'=>'3', 'ehime.jp'=>'3', 'kochi.jp'=>'3', 'fukuoka.jp'=>'3',
		'saga.jp'=>'3', 'nagasaki.jp'=>'3', 'kumamoto.jp'=>'3', 'oita.jp'=>'3',
		'miyazaki.jp'=>'3', 'kagoshima.jp'=>'3', 'okinawa.jp'=>'3', 'sapporo.jp'=>'3',
		'sendai.jp'=>'3', 'chiba.jp'=>'3', 'yokohama.jp'=>'3', 'kawasaki.jp'=>'3',
		'nagoya.jp'=>'3', 'kyoto.jp'=>'3', 'osaka.jp'=>'3', 'kobe.jp'=>'3',
		'hiroshima.jp'=>'3', 'fukuoka.jp'=>'3', 'kitakyushu.jp'=>'3',
		#台湾
		'com.tw'=>'3', 'net.tw'=>'3', 'org.tw'=>'3', 'idv.tw'=>'3', 'game.tw'=>'3',
		'ebiz.tw'=>'3', 'club.tw'=>'3',
		#中国
		'com.cn'=>'3', 'net.cn'=>'3', 'org.cn'=>'3', 'gov.cn'=>'3', 'ac.cn'=>'3',
		'edu.cn'=>'3'
	);
	my %OrgLogNoList = ();
	my %IpList = &ReadIpList;
	for my $i (keys %remote_host) {
		my $host = lc $remote_host{$i};
		if($host =~ /[^0-9\.]/) {
			my($level3, $level2, $level1) = $host =~ /([^\.]+)\.([^\.]+)\.([^\.]+)$/;
			my $org_domain;
			if(my $dom_level = $tld_fix{$level1}) {
				if($dom_level eq '2') {
					$org_domain = "${level2}.${level1}";
				} else {
					$org_domain = "${level3}.${level2}.${level1}";
				}
			} elsif($sld_fix{"${level2}.${level1}"}) {
				$org_domain = "${level3}.${level2}.${level1}";
			} else {
				$org_domain = "${level2}.${level1}";
			}
			$OrgLogNoList{"$org_domain"} .= "$i,";
		} else {
			my $domain = &GetDomainByAddr($host, \%IpList);
			$OrgLogNoList{$domain} .= "$i,";
		}
	}
	my($Org, @NoList, $Views, $Sessions, $Unique);
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for $Org (keys %OrgLogNoList) {
		$OrgLogNoList{$Org} =~ s/,$//;
		@NoList = split(/,/, $OrgLogNoList{$Org});
		$Views = @NoList;
		$PageViewNumList{$Org} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$Org} = $Sessions;
		$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$Org} = $Unique;
	}
	my %OrgList = &ReadDef('./data/organization.dat');
	my($Str1, $Str2, $Domain);
	for $Domain (keys %OrgList) {
		($Str1, $Str2) = split(/,/, $OrgList{$Domain});
		if($Str2) {
			$OrgList{$Domain} = "$Str1<br><div class=\"size2\">（$Str2）";
		} else {
			$OrgList{$Domain} = "$Str1";
		}
	}
	my $Str = '';
	$Str .= "ページビュー<br>\n";
	my @Titles = ('順位', 'ドメイン名', '組織名', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph2(\%PageViewNumList, \@Titles, \%OrgList);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	@Titles = ('順位', 'ドメイン名', '組織名', '訪問数', 'グラフ');
	$Str .= &MakeGraph2(\%SessionNumList, \@Titles, \%OrgList);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	@Titles = ('順位', 'ドメイン名', '組織名', '訪問者数', 'グラフ');
	$Str .= &MakeGraph2(\%UniqueNumList, \@Titles, \%OrgList);
	my $Title = 'アクセス元組織名ランキング';
	&PrintResult($Title, $Str);
}

sub GetDomainByAddr {
	my($addr, $list_ref) = @_;
	$addr =~ m/^([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)$/;
	my $bin = unpack("B32", pack("c4", $1, $2, $3, $4));
	my $flag = 0;
	for my $mask_bin (keys %$list_ref) {
		if($bin =~ /^$mask_bin/) {
			return $$list_ref{$mask_bin};
			last;
		} else {
			next;
		}
	}
	return '?';
}

sub ReadIpList {
	open(IP, './data/ipaddr.dat') || &ErrorPrint("IPアドレスデータファイル ipaddr.dat をオープンできませんでした。 : $!");
	my %ip_list;
	while(<IP>) {
		chop;
		if(/^([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)(\/([0-9]+))*\=(.+)$/) {
			my $ip1 = $1;
			my $ip2 = $2;
			my $ip3 = $3;
			my $ip4 = $4;
			my $mask = $6;
			my $domain = $7;
			my $bin = unpack("B32", pack("c4", $ip1, $ip2, $ip3, $ip4));
			unless($mask) {
				if($ip4 eq '0') {
					$mask = '24';
				} else {
					$mask = 32;
				}
			}
			my $mask_bin = substr($bin, 0, $mask);
			$ip_list{$mask_bin} = $domain;
		} else {
			next;
		}
	}
	close(IP);
	return %ip_list;
}

sub NewVsReturningVisitors {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my $min_date = 99999999999999;
	my $max_date = 0;
	my(%remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		next unless(&IsInDate($date_part));
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		$max_date = $date_part;
		if($i == 0) {$min_date = $date_part;}
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %RepeaterCookies = ();
	my(@CookieParts, $AccessDate, $Sec, $Min, $Hour, $Day, $Mon, $Year);
	for my $i (keys %cookies) {
		@CookieParts = split(/\./, $cookies{$i});
		($Sec, $Min, $Hour, $Day, $Mon, $Year) = localtime($CookieParts[4] + $CONF{'TIMEDIFF'}*60*60);
		$Year += 1900;
		$Mon ++;
		if($Mon < 10) {$Mon = "0$Mon";}
		if($Day < 10) {$Day = "0$Day";}
		if($Hour < 10) {$Hour = "0$Hour";}
		if($Min < 10) {$Min = "0$Min";}
		if($Sec < 10) {$Sec = "0$Sec";}
		$AccessDate = $Year.$Mon.$Day.$Hour.$Min.$Sec;
		if($AccessDate < $min_date) {
			$RepeaterCookies{$cookies{$i}} ++;
		}
	}

    # 総ユニークユーザー数を調べる。
    my $AllUniqueUserNum = &GetUniqueUserNum(\@LogNoList, \%remote_host, \%cookies);
	my($RepeaterUserNum);
	$RepeaterUserNum = scalar keys %RepeaterCookies;

	my @Keys = (
		'初めての訪問者数',
		'リピーター訪問者数',
		'総訪問者数'
	);
	my %Data = (
		'初めての訪問者数' => $AllUniqueUserNum - $RepeaterUserNum,
		'リピーター訪問者数' => $RepeaterUserNum,
		'総訪問者数' => $AllUniqueUserNum
	);
	my($Str);
	$Str .= &MakeTable(\@Keys, \%Data);
	$Str .= "<hr>\n";

	%Data = ('初めての訪問者'=>$AllUniqueUserNum - $RepeaterUserNum, 'リピーター'=>$RepeaterUserNum);
	$Str .= &MakeCircleGraph(\%Data);
	my $Title = 'リピーター比率分析';
	&PrintResult($Title, $Str);
}

sub TopPagesByViews {
	&AnalyzeRequestResource('view');
} 

sub TopPagesByVisits {
	&AnalyzeRequestResource('session');
} 

sub TopPagesByVisitors {
	&AnalyzeRequestResource('unique');
}
	
sub AnalyzeRequestResource {
	my($MODE) = @_;
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, %request, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part, $request_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
			$request_part = $5;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$request_part =~ s/\%7E/\~/ig;
		if($CONF{'URLHANDLE'}) {
			$request_part =~ s/\?.*$//;
		}
		$request{$i} = $request_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %LogNoListBuff = ();	
	for my $i (keys %request) {
		my($HtmlFilePath, $Index, $HitFlag, $FileTest, $uri, $RequestPath);
		if($request{$i} eq '' || $request{$i} eq '-') {next;}
		if($request{$i} =~ /\/$/) {
			unless($request{$i}) {next;}
			$_ = $request{$i};
			m|https*://[^/]+/(.*)|;
			$RequestPath = '/'.$1;
			if($CONF{'URL2PATH_FLAG'}) {
				my $key;
				for $key (keys %URL2PATH) {
					if($request{$i} =~ /^$key/) {
						$HtmlFilePath = $request{$i};
						$HtmlFilePath =~ s/^$key/$URL2PATH{$key}/;
						last;
					}
				}
			} else {
				$HtmlFilePath = $ENV{'DOCUMENT_ROOT'}.$RequestPath;
			}

			$HitFlag = 0;
			for $Index (@DIRECTORYINDEX) {
				$FileTest = $HtmlFilePath.$Index;
				if(-e $FileTest) {
					$uri = $request{$i}.$Index;
					$HitFlag = 1;
					last;
				}
			}
			unless($HitFlag) {$uri = $request{$i};}
		} else {
		    $uri = $request{$i};
		}
		$LogNoListBuff{$uri} .= "$i,";
	}
	my($HtmlTitle);
	my %LogNoList = ();
	my %ManualTitle = &ReadTitleDat;
	for my $uri (keys %LogNoListBuff) {
		my $HtmlTitle = $ManualTitle{$uri};
		unless($HtmlTitle) {
			$HtmlTitle = &GetHtmlTitle("$uri");
		}
		unless($HtmlTitle) {$HtmlTitle = '<i>不明</i>'}
		$LogNoList{"$HtmlTitle<br><div class=\"size2\"><a href=\"$uri\" target=\"blank\">$uri</a></div>"} = $LogNoListBuff{$uri};
	}
	my(@NoList, $Views, $Sessions, $Unique);
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for my $Path (keys %LogNoList) {
		$LogNoList{$Path} =~ s/,$//;
		@NoList = split(/,/, $LogNoList{$Path});
		if($MODE eq 'view') {
			$Views = @NoList;
			$PageViewNumList{$Path} = $Views;
		} elsif($MODE eq 'session') {
			$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
			$SessionNumList{$Path} = $Sessions;
		} elsif($MODE eq 'unique') {
			$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
			$UniqueNumList{$Path} = $Unique;
		}
	}
	my($Str, $Title);
	if($MODE eq 'view') {
		$Str .= "ページビュー<br>\n";
		my(@Titles) = ('順位', 'ページ', 'ページビュー', 'グラフ');
		$Str .= &MakeGraph(\%PageViewNumList, \@Titles);
		$Title = 'アクセスページランキング（ページビュー解析）';
	} elsif($MODE eq 'session') {
		$Str .= "訪問数（セッション数）<br>\n";
		my(@Titles) = ('順位', 'ページ', '訪問数', 'グラフ');
		$Str .= &MakeGraph(\%SessionNumList, \@Titles);
		$Title = 'アクセスページランキング（セッション数解析）';
	} elsif($MODE eq 'unique') {
		$Str .= "訪問者数（ユニークユーザー数）<br>\n";
		my(@Titles) = ('順位', 'ページ', '訪問者数', 'グラフ');
		$Str .= &MakeGraph(\%UniqueNumList, \@Titles);
		$Title = 'アクセスページランキング（訪問者数解析）';
	}

	&PrintResult($Title, $Str);
}

sub VisitorTrace {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %request, %referer, %user_agent, %screen, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $request_part, $referer_part, $ua_part, $accept_lang_part, $screen_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$request_part = $5;
			$referer_part = $6;
			$ua_part = $7;
			$accept_lang_part = $8;
			$screen_part = $9;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		if($TARGET_VISITOR) {
			if($host_part eq $TARGET_VISITOR) {
				$request{$i} = $request_part;
				$referer{$i} = $referer_part;
				$user_agent{$i} = $ua_part;
				$screen{$i} = $screen_part;
			}
		}
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my $TraceDomain = $q->param('TRACEDOMAIN');
	my %VisitorList = ();
	for my $i (keys(%remote_host)) {
		$VisitorList{$remote_host{$i}} ++;
	}
	my($PrintStr);
	$PrintStr .= "<form action=\"$CGI_URL\" method=\"POST\" target=\"_self\">\n";
	$PrintStr .= "<input type=\"hidden\" name=\"FRAME\" value=\"result\">\n";
	$PrintStr .= "<input type=\"hidden\" name=\"ITEM\" value=\"VisitorTrace\">\n";
	$PrintStr .= "<input type=\"hidden\" name=\"LOG\" value=\"$TARGET_LOGNAME\">\n";
	$PrintStr .= "<input type=\"hidden\" name=\"TRACEDOMAIN\" value=\"$TraceDomain\">\n";
	if($ANA_MONTH) {
		$PrintStr .= "<input type=\"hidden\" name=\"MONTH\" value=\"$ANA_MONTH\">\n";
		if($ANA_DAY) {
			$PrintStr .= "<input type=\"hidden\" name=\"DAY\" value=\"$ANA_DAY\">\n";
		}
	}

	$PrintStr .= "<select size=\"1\" name=\"VISITOR\">\n";
	$PrintStr .= "<option value=\"\">ホストを選択して下さい</option>\n";
	my $visitor;
	foreach $visitor (ValueSort(\%VisitorList)) {
		if($TraceDomain) {
			unless($visitor =~ /$TraceDomain/) {next;}
		}
		$PrintStr .= "<option value=\"$visitor\"";
		if($visitor eq $TARGET_VISITOR) {
			$PrintStr .= " selected";
		}
		$PrintStr .= ">$visitor ($VisitorList{$visitor})</option>\n";
	}
	$PrintStr .= "</select>\n";
	$PrintStr .= "<input type=\"submit\" value=\"追跡\" name=\"B1\">\n";
	$PrintStr .= "</form>\n";

	$PrintStr .= "<form action=\"$CGI_URL\" method=\"POST\" target=\"_self\">\n";
	$PrintStr .= "<input type=\"hidden\" name=\"FRAME\" value=\"result\">\n";
	$PrintStr .= "<input type=\"hidden\" name=\"ITEM\" value=\"VisitorTrace\">\n";
	$PrintStr .= "<input type=\"hidden\" name=\"LOG\" value=\"$TARGET_LOGNAME\">\n";
	if($ANA_MONTH) {
		$PrintStr .= "<input type=\"hidden\" name=\"MONTH\" value=\"$ANA_MONTH\">\n";
		if($ANA_DAY) {
			$PrintStr .= "<input type=\"hidden\" name=\"DAY\" value=\"$ANA_DAY\">\n";
		}
	}
	$PrintStr .= "<table border=\"0\"><tr>\n";
	$PrintStr .= "<td>ドメイン名から絞込み検索</td>\n";
	$PrintStr .= "<td><input type=\"text\" name=\"TRACEDOMAIN\" value=\"$TraceDomain\"></td>\n";
	$PrintStr .= "<td><input type=\"submit\" value=\"検索\"></td>\n";
	$PrintStr .= "</tr></table>\n";
	$PrintStr .= "</form>\n";

	if($TARGET_VISITOR) {
		$PrintStr .= "<hr>\n";
		$PrintStr .= "■ 訪問者情報<br>\n";
		my($i, $UserAgent, $ScreenInfo, $FirstNo);
		my $FirstFlag = 0;
		for $i (sort{$a <=> $b} keys %request) {
			unless($FirstFlag) {
				$FirstNo = $i;
				$FirstFlag = 1;
			}
			$UserAgent = $user_agent{$i};
			$ScreenInfo = $screen{$i};
			unless($ScreenInfo) {
				$ScreenInfo = '&nbsp;';
			} else {
				$ScreenInfo =~ s/ /×/g;
			}
		}
		my $ReferUrl = $referer{$FirstNo};

		#OS,ブラウザーを特定
		my ($OS, $OS_V, $BR, $BR_V) = &User_Agent($UserAgent);
		unless($OS) {$OS = '&nbsp;';}
		unless($OS_V) {$OS_V = '&nbsp;';}
		unless($BR) {$BR = '&nbsp;';}
		unless($BR_V) {$BR_V = '&nbsp;';}

		my @HostParts = split(/\./, $TARGET_VISITOR);
		my $Part1 = lc pop(@HostParts);
		my $Part2 = lc pop(@HostParts);
		my $Part3 = lc pop(@HostParts);

		#アクセス元国名（TLD）の特定
		my $CountryStr;
		unless($Part1 =~ /[0-9]/) {
			my %TldList = &ReadDef('./data/country_code.dat');
			$CountryStr = $TldList{$Part1}.'('.$Part1.')';
			undef %TldList;
		}
		unless($CountryStr) {$CountryStr = '&nbsp;';}

		#アクセス元都道府県名、組織名の特定
		my %OrgList = &ReadDef('./data/organization.dat');
		my ($GetPref, $DomainTmp, $Str1, $Str2);

		if(length($Part1) >= 3) {
			$DomainTmp = "$Part2.$Part1";
		} elsif($Part1 eq 'jp') {
			my @AreaList = ('hokkaido', 'aomori', 'iwate', 'miyagi', 'akita', 'yamagata', 'fukushima',
				'ibaraki', 'tochigi', 'gunma', 'saitama', 'chiba', 'tokyo', 'kanagawa',
				'niigata', 'toyama', 'ishikawa', 'fukui', 'yamanashi', 'nagano', 'gifu',
				'shizuoka', 'aichi', 'mie', 'shiga', 'kyoto', 'osaka', 'hyogo', 'nara',
				'wakayama', 'tottori', 'shimane', 'okayama', 'hiroshima', 'yamaguchi',
				'tokushima', 'kagawa', 'ehime', 'kochi', 'fukuoka', 'saga', 'nagasaki',
				'kumamoto', 'oita', 'miyazaki', 'kagoshima', 'okinawa', 'sapporo',
				'sendai', 'chiba', 'yokohama', 'kawasaki', 'nagoya', 'kyoto', 'osaka',
				'kobe', 'hiroshima', 'fukuoka', 'kitakyushu');

			if(length($Part2) ==2 || grep(/^$Part2$/, @AreaList)) {
				$DomainTmp = "$Part3.$Part2.$Part1";
			} else {
				$DomainTmp = "$Part2.$Part1";
			}
		} else {
			$DomainTmp = "$Part2.$Part1";
		}

		($Str1, $Str2, $GetPref) = split(/,/, $OrgList{$DomainTmp});
		undef %OrgList;
		my $Organization = "$Str1";
		unless($Organization) {$Organization = '&nbsp;';}
		if($Str2) {
			$Organization .= "<div class=\"size2\">($Str2)</div>";
		}
		unless($GetPref) {
			my %PrefList = &ReadDef('./data/pref.dat');
			my $host = lc $TARGET_VISITOR;
			my $PrefKeyword = &GetPrefKeyword($host);
			$GetPref = $PrefList{$PrefKeyword};
			undef %PrefList;
		}
		unless($GetPref) {$GetPref = '&nbsp;';}

		my @Keys = (
			'ホスト名',
			'国（TLD）',
			'都道府県',
			'組織名',
			'HTTP_USER_AGENT',
			'プラットフォーム',
			'ブラウザ',
			'画面解像度情報',
		);
		&jcode::convert(\$UserAgent, 'sjis');
		my %Data = (
			'ホスト名' => $TARGET_VISITOR,
			'国（TLD）' => $CountryStr,
			'都道府県' => $GetPref,
			'組織名', => $Organization,
			'HTTP_USER_AGENT' => $UserAgent,
			'プラットフォーム' => "$OS $OS_V",
			'ブラウザ' => "$BR $BR_V",
			'画面解像度情報' => $ScreenInfo
		);
		$PrintStr .= &MakeTable(\@Keys, \%Data);
		$PrintStr .= "<hr>\n";
		my $SessionNo = 1;
		my $DspReferUrl = $ReferUrl;
		if(length($ReferUrl) > 50) {
			$DspReferUrl = substr($ReferUrl, 0, 50) . '...';
		}
		$PrintStr .= "■ 閲覧ページ追跡<br>\n";
		$PrintStr .= "<table border=\"0\" cellspacing=\"0\" cellpadding=\"2\">\n";
		$PrintStr .= "<tr><td colspan=\"3\" bgcolor=\"#3A6EA5\" CLASS=\"ListHeader\">セッション $SessionNo</td></tr>\n";
		$PrintStr .= "<tr bgcolor=\"#EAEAEA\"><td><img src=\"$CONF{'IMAGE_URL'}/refer.gif\" width=\"17\" height=\"17\"></td><td> リンク元</td><td>";
		if($ReferUrl eq '-' || $ReferUrl eq '') {
			$PrintStr .= "$DspReferUrl";
		} else {
			$PrintStr .= "<a href=\"$ReferUrl\" target=\"_blank\">$DspReferUrl</a>";
		}
		$PrintStr .= "</td></tr>\n";
		my($IntervalSec, $PreNo, $DspDate, $DspRequestUrl);
		my %ManualTitle = &ReadTitleDat;
		for $i (sort{$a <=> $b} keys %request) {
			unless($i == $FirstNo) {
				$IntervalSec = &GetRangeSecond($date{$PreNo}, $date{$i});
				if($IntervalSec <= $CONF{'INTERVAL'}) {
					$PrintStr .= "<tr bgcolor=\"#E6EAF3\"><td colspan=\"3\" align=\"right\">$IntervalSec秒 <img src=\"$CONF{'IMAGE_URL'}/timer.gif\" width=\"17\" height=\"17\"></td></tr>\n";
				} else {
					$PrintStr .= "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";
					$PrintStr .= "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";
					$SessionNo ++;
					$PrintStr .= "<tr><td colspan=\"3\" bgcolor=\"#3A6EA5\" CLASS=\"ListHeader\">セッション $SessionNo</td></tr>\n";
					$DspReferUrl = $referer{$i};
					if(length($referer{$i}) > 50) {
						$DspReferUrl = substr($referer{$i}, 0, 50) . '...';
					}
					$PrintStr .= "<tr bgcolor=\"#EAEAEA\"><td><img src=\"$CONF{'IMAGE_URL'}/refer.gif\" width=\"17\" height=\"17\"></td><td> リンク元</td><td>";
					if($referer{$i} eq '-' || $referer{$i} eq '') {
						$PrintStr .= "$DspReferUrl";
					} else {
						$PrintStr .= "<a href=\"$referer{$i}\" target=\"_blank\">$DspReferUrl</a>";
					}
					$PrintStr .= "</td></tr>\n";
				}
			}
			$DspDate = &ConvDspDate($date{$i});
			if(length($request{$i}) > 50) {
				$DspRequestUrl = substr($request{$i}, 0, 50) . '...';
			} else {
				$DspRequestUrl = $request{$i};
			}
			$PrintStr .= "<tr bgcolor=\"#EBE1E2\">\n";
			$PrintStr .= "  <td><img src=\"$CONF{'IMAGE_URL'}/file.gif\" width=\"17\" height=\"17\"></td>\n";
			$PrintStr .= "  <td> $DspDate</td>\n";
			if($request{$i} eq '-' || $request{$i} eq '') {
				$PrintStr .= "  <td> $DspRequestUrl</td>\n";
			} else {
				$PrintStr .= "  <td> <a href=\"$request{$i}\" target=\"_blank\">$DspRequestUrl</a></td>\n";
			}
			$PrintStr .= "</tr>\n";
			$PreNo = $i;
		}
		$PrintStr .= "</table>\n";
	}
	my $Title = "訪問者追跡";
	&PrintResult($Title, $PrintStr);

}


sub ActivityByDayOfTheMonth {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList, $lastdate);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$lastdate = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my($ThisYear, $ThisMonth) = $lastdate =~ /^(\d{4})(\d{2})/;
	my($Y, $M, $D, @DateBuff);
	my %LogNoList = ();	
	for my $i (keys %date) {
		unless($date{$i}) {next;}
		if($date{$i} eq '-') {next;}
		unless($ANA_MONTH) {
			unless($date{$i} =~ /^$ThisYear$ThisMonth/) {next;}
		}
		($Y, $M, $D) = $date{$i} =~ /^(\d{4})(\d{2})(\d{2})/;
		$D =~ s/^0//;
		$LogNoList{$D} .= "$i,";
	}
	my($WeekNum, $DateStr, $Date, @NoList, $Views, $Sessions, $Unique);
	my $LastDayOfThisMonth = &LastDay($ThisYear, $ThisMonth);
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	my @DateList = ();
	my @WeekMap = ('日', '月', '火', '水', '木', '金', '土');
	for (my $i=0;$i<$LastDayOfThisMonth;$i++) {
		$Date = $i + 1;
		$LogNoList{$Date} =~ s/,$//;
		@NoList = split(/,/, $LogNoList{$Date});
		$Views = @NoList;
		$PageViewNumList{$i} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$i} = $Sessions;
		$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$i} = $Unique;
		$WeekNum = &Youbi($ThisYear, $ThisMonth, $Date);
		$DateStr = "$ThisYear年$ThisMonth月$Date日（";
		if($WeekNum == 0) {
			$DateStr .= "<font color=\"#FF0000\">$WeekMap[$WeekNum]</font>）";
		} elsif($WeekNum == 6) {
			$DateStr .= "<font color=\"#0000FF\">$WeekMap[$WeekNum]</font>）";
		} else {
			$DateStr .= "$WeekMap[$WeekNum]）";
		}
		push(@DateList, $DateStr);
	}
	my($Str);
	$Str .= "ページビュー<br>\n";
	my @Titles = ('日付', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph3(\%PageViewNumList, \@Titles, \@DateList);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	@Titles = ('日付', '訪問数', 'グラフ');
	$Str .= &MakeGraph3(\%SessionNumList, \@Titles, \@DateList);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	@Titles = ('日付', '訪問者数', 'グラフ');
	$Str .= &MakeGraph3(\%UniqueNumList, \@Titles, \@DateList);
	my $Title = '日別アクセス数';
	&PrintResult($Title, $Str);

}


sub ActivityByDayOfTheWeek {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %LogNoList = ();
	my($Y, $M, $D, @DateBuff);
	for my $i (keys %date) {
		unless($date{$i}) {next;}
		if($date{$i} eq '-') {next;}
		($Y, $M, $D) = $date{$i} =~ /^(\d{4})(\d{2})(\d{2})/;
		$M =~ s/^0//;
		$D =~ s/^0//;
		@DateBuff = localtime(timelocal(0, 0, 0, $D, $M - 1, $Y));
		$LogNoList{$DateBuff[6]} .= "$i,";
	}
	my(@NoList, $Views, $Sessions, $Unique);

	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for (my $Youbi=0;$Youbi<7;$Youbi++) {
		$LogNoList{$Youbi} =~ s/,$//;
		@NoList = split(/,/, $LogNoList{$Youbi});
		$Views = @NoList;
		$PageViewNumList{$Youbi} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$Youbi} = $Sessions;
		$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$Youbi} = $Unique;
	}
	my($Str);
	my @WeekMap = ('日', '月', '火', '水', '木', '金', '土');
	$Str .= "ページビュー<br>\n";
	my @Titles = ('曜日', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph3(\%PageViewNumList, \@Titles, \@WeekMap);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	@Titles = ('曜日', '訪問数', 'グラフ');
	$Str .= &MakeGraph3(\%SessionNumList, \@Titles, \@WeekMap);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	@Titles = ('曜日', '訪問者数', 'グラフ');
	$Str .= &MakeGraph3(\%UniqueNumList, \@Titles, \@WeekMap);
	my $Title = '曜日別アクセス数';
	&PrintResult($Title, $Str);
}


sub ActivityByHourOfTheDay {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %LogNoList = ();
	my($H, @DateBuff);
	for my $i (keys %date) {
		unless($date{$i}) {next;}
		if($date{$i} eq '-') {next;}
		$H = substr($date{$i}, 8, 2);
		$H =~ s/^0//;
		$LogNoList{$H} .= "$i,";
	}
	my(@NoList, $Views, $Sessions, $Unique);

	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for (my $Hour=0;$Hour<24;$Hour++) {
		$LogNoList{$Hour} =~ s/,$//;
		@NoList = split(/,/, $LogNoList{$Hour});
		$Views = @NoList;
		$PageViewNumList{$Hour} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$Hour} = $Sessions;
		$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$Hour} = $Unique;
	}
	my($Str);
	$Str .= "ページビュー<br>\n";
	my @Titles = ('時間', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph3(\%PageViewNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	@Titles = ('時間', '訪問数', 'グラフ');
	$Str .= &MakeGraph3(\%SessionNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .=	"訪問者数（ユニークユーザー数）<br>\n";
	@Titles = ('時間', '訪問者数', 'グラフ');
	$Str .= &MakeGraph3(\%UniqueNumList, \@Titles);
	my $Title = '時間別アクセス数';
	&PrintResult($Title, $Str);
}

sub TopReferringSites {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, %referer, $host_part, $cookie_part, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $referer_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$referer_part = $6;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		$referer{$i} = $referer_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);
	my %LogNoListBuff = ();
	for my $i (keys %referer) {
		unless($referer{$i}) {next;}
		if($referer{$i} eq '-') {next;}
		my $Flag = 0;
		if(scalar @MY_SITE_URLs) {
			for my $ExceptUrl (@MY_SITE_URLs) {
				if($referer{$i} =~ /^$ExceptUrl/i) {
					$Flag = 1;
					last;
				}
			}
		}
		if($Flag) {next;}
		my $host = lc $referer{$i};
		my @UrlParts = split(/\//, $host);
		my $SiteUrl = "$UrlParts[0]//$UrlParts[2]/";
		$LogNoListBuff{$SiteUrl} .= "$i,";
	}

	my %LogNoList = ();
	my %SiteList = &ReadDef('./data/site.dat');
	for my $key (keys %LogNoListBuff) {
		my $KeyStr;
		my $SiteName = &GetSiteName(\%SiteList, $key, 1);
		my $EncodedUrl = &URL_Encode($key);
		my $LinkUrl = "${CGI_URL}?REDIRECT=$EncodedUrl";
		if($SiteName) {
			$KeyStr = "$SiteName<br>";
			$KeyStr .= "<div class=\"size2\"><a href=\"$LinkUrl\" target=\"_blank\">$key</a></div>";
		} else {
			$KeyStr .= "<a href=\"$LinkUrl\" target=\"_blank\">$key</a>";
		}
		$LogNoList{$KeyStr} = $LogNoListBuff{$key};
	}
	my %SessionNumList = ();
	for my $key (keys %LogNoList) {
		$LogNoList{$key} =~ s/,$//;
		my @NoList = split(/,/, $LogNoList{$key});
		my $Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$key} = $Sessions;
	}
	my @Titles = ('順位', 'URL', '訪問数', 'グラフ');
	my $Str = &MakeGraph(\%SessionNumList, \@Titles);
	my $Title = 'リンク元サイトランキング';
	&PrintResult($Title, $Str);
}

sub GetSiteName {
	my($site_hash_ref, $url, $site_flag) = @_;
	if($site_flag) {
		my @url_parts = split(/\//, $url);
		$url = $url_parts[2];
	}
	my $domain;
	my $hit_domain;
	for $domain (keys %$site_hash_ref) {
		if($site_flag) {
			if($domain =~ /\//) {next;}
		}
		if($url =~ /$domain/) {
			#my $site_name = $site_hash_ref->{$url};
			#return $site_name;
			#last;
			if(length($domain) > length($hit_domain)) {
				$hit_domain = $domain;
			}
		}
	}
	return $site_hash_ref->{$hit_domain};
}

sub TopReferringURLs {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, %referer, $host_part, $cookie_part, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $referer_part, $host_part, $cookie_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$referer_part = $6;
			$host_part = $2;
			$cookie_part = $3;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$cookies{$i} = $cookie_part;
		$referer{$i} = $referer_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %LogNoListBuff = ();
	for my $i (keys %referer) {
		unless($referer{$i}) {next;}
		if($referer{$i} eq '-') {next;}
		my $Flag = 0;
		if(scalar @MY_SITE_URLs) {
			my $ExceptUrl;
			for $ExceptUrl (@MY_SITE_URLs) {
				if($referer{$i} =~ /^$ExceptUrl/i) {
					$Flag = 1;
					last;
				}
			}
		}
		if($Flag) {next;}
		$LogNoListBuff{$referer{$i}} .= "$i,";
	}
	my %SiteList = &ReadDef('./data/site.dat');
	my %LogNoList = ();
	for my $key (keys %LogNoListBuff) {
		my $DspUrl;
		if(length($key) > 50) {
			$DspUrl = substr($key, 0, 50);
			$DspUrl .= '...';
		} else {
			$DspUrl = $key;
		}
		my $SiteName = &GetSiteName(\%SiteList, $key);
		my $KeyStr;
		my $EncodedUrl = &URL_Encode($key);
		my $LinkUrl = "${CGI_URL}?REDIRECT=$EncodedUrl";
		if($SiteName) {
			$KeyStr = "$SiteName<br>";
			$KeyStr .= "<div class=\"size2\"><a href=\"$LinkUrl\" target=\"_blank\">$DspUrl</a></div>";
		} else {
			$KeyStr .= "<a href=\"$LinkUrl\" target=\"_blank\">$DspUrl</a>";
		}
		$LogNoList{$KeyStr} = $LogNoListBuff{$key};	
	}
	my(@NoList, $Sessions);
	my %SessionNumList = ();
	for my $key (keys %LogNoList) {
		$LogNoList{$key} =~ s/,$//;
		@NoList = split(/,/, $LogNoList{$key});
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$key} = $Sessions;
	}
	my @Titles = ('順位', 'URL', '訪問数', 'グラフ');
	my $Str = &MakeGraph(\%SessionNumList, \@Titles);
	my $Title = 'リンク元URLランキング';
	&PrintResult($Title, $Str);
}

sub TopSearchKeywords {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%referer, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $referer_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$referer_part = $6;
		} else {
			next;
		}
		next if($date_part eq '');
		next unless(&IsInDate($date_part));
		$referer{$i} = $referer_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);
	my %KeywordCount = ();	
	for my $i (keys %referer) {
		if($referer{$i} eq '' || $referer{$i} eq '-') {
			next;
		}
		if($referer{$i} =~ /\?/) {
			my($keyword) = &GetSearchKeyword($referer{$i});
			if($keyword ne '') {
				$keyword =~ s/</&lt;/g;
				$keyword =~ s/>/&gt;/g;
				$KeywordCount{$keyword} ++;
			}
		} else {
			next;
		}
	}
	my @Titles = ('順位', 'キーワード', '訪問数', 'グラフ');
	my $Str = &MakeGraph(\%KeywordCount, \@Titles);
	my $Title = '検索キーワードランキング';
	&PrintResult($Title, $Str);
}

sub TopSearchEngines {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%referer, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $referer_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$referer_part = $6;
		} else {
			next;
		}
		next if($date_part eq '');
		next unless(&IsInDate($date_part));
		$referer{$i} = $referer_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %engine_list = ();
	my %keyword_list = ();
	my %engine_urls = ();
	my $sum = 0;
	for my $i (keys %referer) {
		if($referer{$i} eq '' || $referer{$i} eq '-') {
			next;
		}
		if($referer{$i} =~ /\?/) {
			my($keyword, $engine_name, $engine_url) = &GetSearchKeyword($referer{$i});
			if($keyword ne '') {
				$keyword =~ s/</&lt;/g;
				$keyword =~ s/>/&gt;/g;
				$engine_list{$engine_name} ++;
				$keyword_list{"$engine_name:$keyword"} ++;
				$engine_urls{$engine_name} = $engine_url;
				$sum ++;
			}
		}
	}

	my $Str;
	$Str .= &MakeCircleGraph(\%engine_list);
	$Str .= "<br>\n";
	$Str .= "<TABLE BORDER=\"0\">\n";
	$Str .= "  <TR BGCOLOR=\"#3A6EA5\">\n";
	$Str .= "    <td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">順位</FONT></td>\n";
	$Str .= "    <td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">検索エンジン</FONT></td>\n";
	$Str .= "    <td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">訪問数</FONT></td>\n";
	$Str .= "    <td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">グラフ</FONT></td>\n";
	$Str .= "  </TR>\n";
	my $engine_order = 1;
	foreach my $key (ValueSort(\%engine_list)) {
		my $rate = int($engine_list{$key} * 10000 / $sum) / 100;
		my $GraphLength = int($CONF{'GRAPHMAXLENGTH'} * $rate / 100);
		$Str .= "  <TR BGCOLOR=\"#EAEAEA\" VALIGN=\"MIDDLE\">\n";
		$Str .= "    <TD ALIGN=\"CENTER\">$engine_order</TD>\n";
		$Str .= "    <TD><a href=\"$engine_urls{$key}\" target=\"_blank\">$key</a></TD>\n";
		$Str .= "    <TD ALIGN=\"RIGHT\">$engine_list{$key}</TD>\n";
		$Str .= "    <TD class=\"size2\">";
		if($rate < 1) {
			$Str .= "";
		} else {
			$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar\.gif\" WIDTH=\"$GraphLength\" HEIGHT=\"10\">";
		}
		$Str .= " ($rate%)</TD>\n";
		$Str .= "  </TR>\n";

		for my $key1 (ValueSort(\%keyword_list)) {
			my($name, $word) = split(/\:/, $key1);
			if($name eq $key) {
				my $rate2 = int($keyword_list{$key1} * 10000 / $sum) / 100;
				my $GraphLength2 = int($CONF{'GRAPHMAXLENGTH'} * $rate2 / 100);
				$Str .= "  <TR class=\"size2\">\n";
				$Str .= "    <TD></TD>\n";
				$Str .= "    <TD BGCOLOR=\"#B7B7B7\"><LI>$word</LI></TD>\n";
				$Str .= "    <TD BGCOLOR=\"#B7B7B7\" ALIGN=\"RIGHT\">$keyword_list{$key1}</TD>\n";
				$Str .= "    <TD BGCOLOR=\"#B7B7B7\">";
				if($rate2 < 1) {
					$Str .= "\&nbsp\;";
				} else {
					$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar2\.gif\" WIDTH=\"$GraphLength2\" HEIGHT=\"8\">";
				}
				$Str .= " ($rate2%)</TD>\n";
				$Str .= "  </TR>\n";
			}
		}
		$engine_order ++;
	}
	$Str .= "</TABLE>\n";
	$Str .= "<BR><BR>\n";

	my $Title = '検索エンジンランキング';
	&PrintResult($Title, $Str);
}

sub GetSearchKeyword {
		my($requested_url) = @_;
		my ($url, $getstr) = split(/\?/, $requested_url);
		if($getstr eq '') {
			return '';
		}
		my @parts = split(/\&/, $getstr);
		my %variables = ();
		my $part;
		for $part (@parts) {
			my ($name, $value) = split(/=/, $part);
			$variables{$name} = $value;
		}
		my @url_parts = split(/\//, $url);
		my @url_parts2 = split(/\./, $url_parts[2]);
		my $tld = pop @url_parts2;
		my $word = '';
		my $engine_name = '';
		my $engine_url = '';
		if($url =~ /lycos/) {
			if($url =~ /wisenut/) {
				$word = $variables{'q'};
			} elsif($url =~ /\.lycos\.co\.jp/) {
				$word = $variables{'q'};
			} else {
				$word = $variables{'query'};
			}
			$engine_name = "Lycos($tld)";
			my @tmp = split(/\.lycos\./, $url);
			my $suffix = pop @tmp;
			$engine_url = 'http://www.lycos.' . $suffix;
		} elsif($url =~ /\.google\./) {
			if($url =~ /images\.google\./) {
				my $prev = $variables{'prev'};
				$prev = &URL_Decode($prev);
				if($prev =~ /q=([^&]+)&/) {
					$word = $1;
				}
			} else {
				$word = $variables{'q'};
			}
			$engine_name = "Google($tld)";
			my @tmp = split(/\.google\./, $url);
			my $suffix = pop @tmp;
			$engine_url = 'http://www.google.' . $suffix;
		} elsif($url =~ /\.yahoo\./) {
			$word = $variables{'p'};
			$engine_name = "Yahoo!($tld)";
			my @tmp = split(/\.yahoo\./, $url);
			my $suffix = pop @tmp;
			$engine_url = 'http://www.yahoo.' . $suffix;
		} elsif($url =~ /\.excite\./) {
			if($url =~ /odn\.excite\.co\.jp/) {
				$word = $variables{'search'};
				$engine_name = "ODN Search";
				$engine_url = 'http://www.odn.ne.jp/';
			} elsif($url =~ /dion\.excite\.co\.jp/) {
				$word = $variables{'search'};
				$engine_name = "DION Search";
				$engine_url = 'http://www.dion.ne.jp/';
			} else {
				$word = $variables{'s'};
				unless($word) {
					$word = $variables{'search'};
				}
				$engine_name = "excite($tld)";
				my @tmp = split(/\.excite\./, $url);
				my $suffix = pop @tmp;
				$engine_url = 'http://www.excite.' . $suffix;
			}
		} elsif($url =~ /\.msn\./) {
			$word = $variables{'q'};
			$engine_name = "MSN($tld)";
			my @tmp = split(/\.msn\./, $url);
			my $suffix = pop @tmp;
			$engine_url = 'http://www.msn.' . $suffix;
		} elsif($url =~ /\.infoseek\./) {
			$word = $variables{'qt'};
			$engine_name = 'infoseek';
			$engine_url = 'http://www.infoseek.co.jp/';
		} elsif($url =~ /\.goo\.ne\.jp/) {
			$word = $variables{'MT'};
			$engine_name = 'goo';
			$engine_url = 'http://www.goo.ne.jp/';
		} elsif($url =~ /\.fresheye\.com/) {
			$word = $variables{'kw'};
			$engine_name = 'フレッシュアイ';
			$engine_url = 'http://www.fresheye.com/';
		} elsif($url =~ /inetg\.com/) {
			$word = $variables{'key'};
			$engine_name = 'iNET Guide';
			$engine_url = 'http://www.inetg.com/';
		} elsif($url =~ /search\.biglobe\.ne\.jp/) {
			$word = $variables{'q'};
			$engine_name = 'BIGLOBEサーチ attayo';
			$engine_url = 'http://search.biglobe.ne.jp/';
		} elsif($url =~ /search\.netscape\.com/) {
			$word = $variables{'query'};
			$engine_name = 'Netscape Search';
			$engine_url = 'http://www.netscape.com/';
		} elsif($url =~ /www\.overture\.com/) {
			$word = $variables{'Keywords'};
			$engine_name = 'overture';
			$engine_url = 'http://www.overture.com/';
		} elsif($url =~ /\.altavista\.com/) {
			$word = $variables{'q'};
			$engine_name = 'altavista';
			$engine_url = 'http://au.altavista.com/';
		} elsif($url =~ /search\.aol\.com/) {
			$word = $variables{'query'};
			$engine_name = 'AOL Search';
			$engine_url = 'http://search.aol.com/';
		} elsif($url =~ /\.looksmart\.com/) {
			$word = $variables{'key'};
			$engine_name = 'looksmart';
			$engine_url = 'http://www.looksmart.com/';
		} elsif($url =~ /www\.infofreako\.com\/factory\/multifind\/multifind\.pl/) {
			$word = $variables{'string'};
			$engine_name = 'multifind';
			$engine_url = 'http://www.infofreako.com/factory/multifind/multifind.pl';
		} elsif($url =~ /bach\.scitec\.kobe-u\.ac\.jp\/cgi-bin\/metcha\.cgi/) {
			$word = $variables{'q'};
			$engine_name = 'Metcha Seearch';
			$engine_url = 'http://bach.scitec.kobe-u.ac.jp/metcha/';
		} elsif($url =~ /\.alltheweb\.com/) {
			$word = $variables{'q'};
			$engine_name = 'alltheweb';
			$engine_url = 'http://www.alltheweb.com/';
		} else {
			return '';
		}

		if($word eq '') {
			return '';
		}
		my $decode_str = &URL_Decode($word);
		if($JFLAG) {
			eval {
				&Jcode::convert(\$decode_str, "sjis");
			}
		} else {
			eval {
				&jcode::convert(\$decode_str, "sjis");
			}
		}
		my @engine_url_parts = split(/\//, $engine_url);
		$engine_url = "http://$engine_url_parts[2]/";
		return $decode_str, $engine_name, $engine_url;
}


sub TopBrowsers {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my $loglines = 0;
	my(%all_date, %date, %user_agent, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $ua_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$ua_part = $7;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$user_agent{$i} = $ua_part;
		push(@LogNoList, $i);
		$i ++;
		$loglines ++;
	}
	close(LOGFILE);
	my(%browser_list, %browser_v_list, %platform_list, %platform_v_list);
	for my $ua (keys %user_agent) {
		my($platform, $platform_v, $browser, $browser_v) = &User_Agent($user_agent{$ua});
		$browser_list{$browser} ++;
		$browser_v_list{"$browser:$browser_v"} ++;
		$platform_list{"$platform"} ++;
		$platform_v_list{"$platform:$platform_v"} ++;
	}

	my($Str);
	$Str .= &MakeCircleGraph(\%browser_list);
	$Str .= "<br>\n";
	$Str .= "<TABLE BORDER=\"0\">\n";
	$Str .= "<TR BGCOLOR=\"#3A6EA5\">\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">順位</FONT></td>\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">ブラウザー</FONT></td>\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">リクエスト数</FONT></td>\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">グラフ</FONT></td></TR>\n";
	my $browser_order = 1;
	foreach my $key (ValueSort(\%browser_list)) {
		my $rate = int($browser_list{$key} * 10000 / $loglines) / 100;
		my $GraphLength = int($CONF{'GRAPHMAXLENGTH'} * $rate / 100);
		$Str .= "<TR BGCOLOR=\"#EAEAEA\" VALIGN=\"MIDDLE\"><TD ALIGN=\"CENTER\">$browser_order</TD><TD>";
		if($key eq '') {
			$Str .= " 不明</TD><TD ALIGN=\"RIGHT\">$browser_list{$key}</TD><TD>";
		} else {
			$Str .= " $key</TD><TD ALIGN=\"RIGHT\">$browser_list{$key}</TD><TD class=\"size2\">";
		}
		if($rate < 1) {
			$Str .= "";
		} else {
			$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar\.gif\" WIDTH=\"$GraphLength\" HEIGHT=\"10\">";
		}
		$Str .= " ($rate%)</TD></TR>\n";

		for my $key1 (sort keys %browser_v_list) {
			if($key1 =~ /^$key:/) {
				my $rate2 = int($browser_v_list{$key1} * 10000 / $loglines) / 100;
				my $GraphLength2 = int($CONF{'GRAPHMAXLENGTH'} * $rate2 / 100);
				my $v = $key1;
				$v =~ s/^$key://;
				$Str .= "<TR class=\"size2\"><TD></TD><TD BGCOLOR=\"#B7B7B7\"><LI>$v</LI></TD><TD BGCOLOR=\"#B7B7B7\" ALIGN=\"RIGHT\">$browser_v_list{$key1}</TD>";
				$Str .= "<TD BGCOLOR=\"#B7B7B7\">";
				if($rate2 < 1) {
					$Str .= "\&nbsp\;";
				} else {
					$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar2\.gif\" WIDTH=\"$GraphLength2\" HEIGHT=\"8\">";
				}
				$Str .= " ($rate2%)</TD></TR>\n";
			}
		}
		$browser_order ++;
	}
	$Str .= "</TABLE>\n";
	$Str .= "<BR><BR>\n";

	my $Title = 'ブラウザーランキング';
	&PrintResult($Title, $Str);
}


sub TopAcceptLanguage {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my(%all_date, %date, %remote_host, %cookies, %accept_language, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part, $accept_lang_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
			$accept_lang_part = $8;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$accept_language{$i} = $accept_lang_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my(%LogNoListBuff) = ();
	for my $i (keys %accept_language) {
		if($accept_language{$i} eq '-') {next;}
		unless($accept_language{$i}) {next;}
		my @buff = split(/,/, $accept_language{$i});
		my $max = 0;
		my($lang);
		for my $j (@buff) {
			my ($lang_tmp, $value_tmp) = split(/\;/, $j);
			$value_tmp =~ s/q=//;
			$value_tmp = 1 if($value_tmp eq '');
			if($max < $value_tmp) {
				$lang = $lang_tmp;
				$max = $value_tmp;
			}
		}
	  	$LogNoListBuff{"\L$lang"} .= "$i,";
	}
	my %LangCodeList = &ReadDef('./data/language.dat');
	my %LogNoList = ();
	for my $key (keys %LogNoListBuff) {
		$LogNoList{$LangCodeList{$key}} = $LogNoListBuff{$key};
	}
	my(@NoList, $Views, $Sessions, $Unique);
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for my $key (keys %LogNoList) {
		$LogNoList{$key} =~ s/,$//;
		@NoList = split(/,/, $LogNoList{$key});
		$Views = @NoList;
		$PageViewNumList{$key} = $Views;
		$Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$key} = $Sessions;
		$Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$key} = $Unique;
	}
	my($Str);
	$Str .= "ページビュー<br>\n";
	$Str .= &MakeCircleGraph(\%PageViewNumList);
	$Str .= "<br>\n";
	my @Titles = ('順位', '言語', 'ページビュー', 'グラフ');
	$Str .=&MakeGraph(\%PageViewNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	$Str .= &MakeCircleGraph(\%SessionNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '言語', '訪問数', 'グラフ');
	$Str .= &MakeGraph(\%SessionNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	$Str .= &MakeCircleGraph(\%UniqueNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '言語', '訪問者数', 'グラフ');
	$Str .= &MakeGraph(\%UniqueNumList, \@Titles);
	my $Title = 'ブラウザー表示言語ランキング';
	&PrintResult($Title, $Str);
}

sub TopPlatforms {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my $loglines = 0;
	my(%all_date, %date, %user_agent, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $ua_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$ua_part = $7;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$user_agent{$i} = $ua_part;
		push(@LogNoList, $i);
		$i ++;
		$loglines ++;
	}
	close(LOGFILE);

	my(%browser_list, %browser_v_list, %platform_list, %platform_v_list);
	for my $ua (keys %user_agent) {
		my ($platform, $platform_v, $browser, $browser_v) = &User_Agent($user_agent{$ua});
		$browser_list{$browser} ++;
		$browser_v_list{"$browser:$browser_v"} ++;
		$platform_list{"$platform"} ++;
		$platform_v_list{"$platform:$platform_v"} ++;
	}

	my($Str);
	$Str .= &MakeCircleGraph(\%platform_list);
	$Str .= "<br>\n";
	$Str .= "<TABLE BORDER=\"0\">\n";
	$Str .= "<TR BGCOLOR=\"#3A6EA5\">\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">順位</FONT></td>\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">Operating System</FONT></td>\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">ページビュー</FONT></td>\n";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">グラフ</FONT></td></TR>\n";
	my $os_order = 1;
	foreach my $key (ValueSort(\%platform_list)) {
		my $rate = int($platform_list{$key} * 10000 / $loglines) / 100;
		my $GraphLength = int($CONF{'GRAPHMAXLENGTH'} * $rate / 100);

		$Str .= "<TR BGCOLOR=\"#EAEAEA\"><TD ALIGN=\"CENTER\">$os_order</TD><TD>";
		if($key eq '') {
			$Str .= " 不明</TD><TD ALIGN=\"RIGHT\">$platform_list{$key}</TD><TD>";
		} else {
			$Str .= " $key</TD><TD ALIGN=\"RIGHT\">$platform_list{$key}</TD><TD class=\"size2\">";
		}
		if($rate < 1) {
			$Str .= "";
		} else {
			$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar\.gif\" WIDTH=\"$GraphLength\" HEIGHT=\"10\">";
		}
		$Str .= " ($rate%)</TD></TR>\n";

		for my $key1 (sort keys %platform_v_list) {
			if($key1 =~ /^$key:/) {
				my $rate2 = int($platform_v_list{$key1} * 10000 / $loglines) / 100;
				my $GraphLength2 = int($CONF{'GRAPHMAXLENGTH'} * $rate2 / 100);
				my $v = $key1;
				$v =~ s/^$key://;
				$Str .= "<TR class=\"size2\">\n";
				$Str .= "<TD></TD><TD BGCOLOR=\"#B7B7B7\"><LI>$v</LI></TD>\n";
				$Str .= "<TD BGCOLOR=\"#B7B7B7\" ALIGN=\"RIGHT\">$platform_v_list{$key1}</TD>\n";
				$Str .= "<TD BGCOLOR=\"#B7B7B7\">";
				if($rate2 < 1) {
					$Str .= "\&nbsp\;";
				} else {
					$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar2\.gif\" WIDTH=\"$GraphLength2\" HEIGHT=\"8\">";
				}
				$Str .= " ($rate2%)</TD></TR>\n";
			}
		}

		$os_order ++;
	}
	$Str .= "</TABLE>\n";
	$Str .= "<BR><BR>\n";

	my $Title = 'ＯＳランキング';
	&PrintResult($Title, $Str);
}


sub TopResolution {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my $min_date = 99999999999999;
	my $max_date = 0;
	my(%all_date, %date, %cookies, %remote_host, %screen, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $cookie_part, $host_part, $screen_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
			$screen_part = $9;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$screen{$i} = $screen_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %LogNoList = ();
	for my $i (keys %screen) {
		if($screen{$i} eq '-') {next;}
		unless($screen{$i}) {next;}
		my($ScreenWidth, $ScreenHeight, $ColorDepth) = split(/\s/, $screen{$i});
	  	$LogNoList{"$ScreenWidth×$ScreenHeight"} .= "$i,";
	}
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for my $key (keys %LogNoList) {
		$LogNoList{$key} =~ s/,$//;
		my @NoList = split(/,/, $LogNoList{$key});
		my $Views = @NoList;
		$PageViewNumList{$key} = $Views;
		my $Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$key} = $Sessions;
		my $Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$key} = $Unique;
	}
	my($Str);
	$Str .= "ページビュー<br>\n";
	$Str .= &MakeCircleGraph(\%PageViewNumList);
	$Str .= "<br>\n";
	my @Titles = ('順位', '解像度', 'ページビュー', 'グラフ');
	$Str .=&MakeGraph(\%PageViewNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	$Str .= &MakeCircleGraph(\%SessionNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '解像度', '訪問数', 'グラフ');
	$Str .= &MakeGraph(\%SessionNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	$Str .= &MakeCircleGraph(\%UniqueNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '解像度', '訪問者数', 'グラフ');
	$Str .= &MakeGraph(\%UniqueNumList, \@Titles);
	my $Title = 'クライアント画面解像度ランキング';
	&PrintResult($Title, $Str);
}


sub TopColorDepth {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my $min_date = 99999999999999;
	my $max_date = 0;
	my(%all_date, %date, %remote_host, %cookies, %screen, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part, $screen_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
			$screen_part = $9;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$screen{$i} = $screen_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %LogNoListBuff = ();
	for my $i (keys %screen) {
		if($screen{$i} eq '-') {next;}
		unless($screen{$i}) {next;}
		my ($ScreenWidth, $ScreenHeight, $ColorDepth) = split(/\s/, $screen{$i});
	  	$LogNoListBuff{$ColorDepth} .= "$i,";
	}
	my %LogNoList = ();
	for my $key (keys %LogNoListBuff) {
		my $KeyStr = 2**$key;
		$KeyStr .= '色';
		$KeyStr .= "（$key bit）";
		$LogNoList{$KeyStr} = $LogNoListBuff{$key};	
	}
	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for my $key (keys %LogNoList) {
		$LogNoList{$key} =~ s/,$//;
		my @NoList = split(/,/, $LogNoList{$key});
		my $Views = scalar @NoList;
		$PageViewNumList{$key} = $Views;
		my $Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$key} = $Sessions;
		my $Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$key} = $Unique;
	}
	my($Str);
	$Str .= "ページビュー<br>\n";
	$Str .= &MakeCircleGraph(\%PageViewNumList);
	$Str .= "<br>\n";
	my @Titles = ('順位', '色深度', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph(\%PageViewNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	$Str .= &MakeCircleGraph(\%SessionNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '色深度', '訪問数', 'グラフ');
	$Str .= &MakeGraph(\%SessionNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	$Str .= &MakeCircleGraph(\%UniqueNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', '色深度', '訪問者数', 'グラフ');
	$Str .= &MakeGraph(\%UniqueNumList, \@Titles);
	my $Title = 'クライアント画面色深度ランキング';
	&PrintResult($Title, $Str);
}

sub TopVideoMemorySize {
	if(-e "$LOGDIR/$TARGET_LOGNAME") {
		open(LOGFILE, "$LOGDIR/$TARGET_LOGNAME") || &ErrorPrint("アクセスログ「$LOGDIR/$TARGET_LOGNAME」をオープンできませんでした");
	} else {
		&ErrorPrint("アクセスログ（$LOGDIR/$TARGET_LOGNAME）がありません。");
	}
	my $i = 0;
	my $min_date = 99999999999999;
	my $max_date = 0;
	my(%all_date, %date, %remote_host, %cookies, %screen, @LogNoList);
	while(<LOGFILE>) {
		chop;
		my($date_part, $host_part, $cookie_part, $screen_part);
		if(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\"([^\"]+)\"\s+\"([^\"]+)\"\s+\"([^\"]+)\"/) {
			$date_part = $1;
			$host_part = $2;
			$cookie_part = $3;
			$screen_part = $9;
		} else {
			next;
		}
		next if($date_part eq '');
		$all_date{$i} = $date_part;
		next unless(&IsInDate($date_part));
		$date{$i} = $date_part;
		$remote_host{$i} = $host_part;
		$screen{$i} = $screen_part;
		$cookies{$i} = $cookie_part;
		push(@LogNoList, $i);
		$i ++;
	}
	close(LOGFILE);

	my %LogNoList = ();
	for my $i (keys %screen) {
		if($screen{$i} eq '-') {next;}
		unless($screen{$i}) {next;}
		my($ScreenWidth, $ScreenHeight, $ColorDepth) = split(/\s/, $screen{$i});
		my $VideoMemorySize = (int($ScreenWidth * $ScreenHeight * $ColorDepth * 10 / 8 / 1024 / 1024)) / 10;
		unless( ($VideoMemorySize*10)%10 == 0) {
			$VideoMemorySize = int($VideoMemorySize) + 1;
		}
	  	$LogNoList{"$VideoMemorySize MB"} .= "$i,";
	}

	my %SessionNumList = ();
	my %PageViewNumList = ();
	my %UniqueNumList = ();
	for my $key (keys %LogNoList) {
		$LogNoList{$key} =~ s/,$//;
		my @NoList = split(/,/, $LogNoList{$key});
		my $Views = @NoList;
		$PageViewNumList{$key} = $Views;
		my $Sessions = &GetSessionNum(\@NoList, \%date, \%remote_host, \%cookies);
		$SessionNumList{$key} = $Sessions;
		my $Unique = &GetUniqueUserNum(\@NoList, \%remote_host, \%cookies);
		$UniqueNumList{$key} = $Unique;
	}
	my($Str);
	$Str .= "ページビュー<br>\n";
	$Str .= &MakeCircleGraph(\%PageViewNumList);
	$Str .= "<br>\n";
	my @Titles = ('順位', 'サイズ', 'ページビュー', 'グラフ');
	$Str .= &MakeGraph(\%PageViewNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問数（セッション数）<br>\n";
	$Str .= &MakeCircleGraph(\%SessionNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', 'サイズ', '訪問数', 'グラフ');
	$Str .= &MakeGraph(\%SessionNumList, \@Titles);
	$Str .= "<hr>\n";
	$Str .= "訪問者数（ユニークユーザー数）<br>\n";
	$Str .= &MakeCircleGraph(\%UniqueNumList);
	$Str .= "<br>\n";
	@Titles = ('順位', 'サイズ', '訪問者数', 'グラフ');
	$Str .= &MakeGraph(\%UniqueNumList, \@Titles);
	my $Title = 'クライアント画面ビデオメモリーランキング';
	&PrintResult($Title, $Str);
}


sub MakeTable {
	my($Keys, $Data) = @_;
	my($key);
	my($Str) = "<TABLE BORDER=\"0\">\n";
	for $key (@$Keys) {
		$Str .= "<TR>\n";
		$Str .= "  <TD BGCOLOR=\"#3A6EA5\" CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$key</FONT></TD>\n";
		$Str .= "  <TD BGCOLOR=\"#EAEAEA\" ALIGN=\"left\">$$Data{$key}</TD>\n";
		$Str .= "</TR>\n";
	}
	$Str .= "</TABLE>\n";
	return $Str;
}


sub GetUniqueUserNum {
	my($no_ref, $host_ref, $cookies_ref) = @_;
	my $i;
	my $UniqueNum = 0;
	my %UniqueCookies = ();
	for my $i (@$no_ref) {
		$UniqueCookies{$$cookies_ref{$i}} ++;
	}
	my $key;
	my %UniqueRemoteHosts = ();
	my %ReverseCookies = reverse %$cookies_ref;
	for my $key (keys(%UniqueCookies)) {
		if($UniqueCookies{$key} > 1) {
			$UniqueNum ++;
		} else {
    		my $No = $ReverseCookies{$key};
    		$UniqueRemoteHosts{$$host_ref{$No}} ++;
		}
	}
	my @TempArray = keys %UniqueRemoteHosts;
	my $TempNum = scalar @TempArray;
	$UniqueNum += $TempNum;
	return $UniqueNum;
}

sub GetSessionNum {
	my($no_ref, $date_ref, $host_ref, $cookies_ref) = @_;
	my($i, $diff);
	my %UniqueCookies = ();
	for my $i (@$no_ref) {
		$UniqueCookies{$$cookies_ref{$i}} ++;
	}
	my %LastAccessDate  = ();
	my %CookieLastAccessDate = ();
	my($SessionNum) = 0;
	for my $i (sort {$a<=>$b} @$no_ref) {
		if($UniqueCookies{$$cookies_ref{$i}} > 1) {
			if(exists($CookieLastAccessDate{$$cookies_ref{$i}})) {
				my $diff = &GetSecDiff($$date_ref{$i}, $CookieLastAccessDate{$$cookies_ref{$i}});
				if($diff > $CONF{'INTERVAL'}) {
					$SessionNum ++;
				}
		    } else {
				$SessionNum ++;
			}
		} else {
			if(exists($LastAccessDate{$$host_ref{$i}})) {
				$diff = &GetSecDiff($$date_ref{$i}, $LastAccessDate{$$host_ref{$i}});
				if($diff > $CONF{'INTERVAL'}) {
					$SessionNum ++;
				}
			} else {
				$SessionNum ++;
			}
		}
		$CookieLastAccessDate{$$cookies_ref{$i}} = $$date_ref{$i};
		$LastAccessDate{$$host_ref{$i}} = $$date_ref{$i};
	}
	return $SessionNum;
}

sub GetSecDiff {
	my(@DateList) = @_;
	my @TimeList = ();
	for my $DateStr (@DateList) {
		my ($Year, $Mon, $Day, $Hour, $Min, $Sec) = $DateStr =~ /^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/;
		$Year -= 1900;
		$Mon =~ s/^0//;	$Mon --;
		$Day =~ s/^0//;
		$Hour =~ s/^0//;
		$Min =~ s/^0//;
		$Sec =~ s/^0//;
		my $Time = timelocal($Sec, $Min, $Hour, $Day, $Mon, $Year);
		push(@TimeList, $Time);
	}
	my $Diff = abs($TimeList[0] - $TimeList[1]);
	return $Diff;
}

sub GetToday {
	my @Date = localtime(time + $CONF{'TIMEDIFF'}*60*60);
	my $Year = $Date[5] + 1900;
	my $Mon = $Date[4] + 1;
	my $Day = $Date[3];
	if($Mon < 10) {$Mon = "0$Mon";}
	if($Day < 10) {$Day = "0$Day";}
	return $Year.$Mon.$Day;
}

# 日時文字列（YYYYMMDDhhmmss）を YYYY/MM/DD hh:mm:ss に変換する
sub ConvDspDate {
	my($DateStr) = @_;
	my($Year, $Mon, $Day, $Hour, $Min, $Sec) = $DateStr =~ /^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/;
	return "$Year/$Mon/$Day $Hour:$Min:$Sec";
}

# 開始時刻と終了時刻を引数とし、その間の秒数を返す。
# 引数は、YYYYMMDDhhmmss 形式
sub GetRangeSecond {
	my($StartStr, $EndStr) = @_;
	my($MinYear, $MinMon, $MinDay, $MinHour, $MinMin, $MinSec) = $StartStr =~ /^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/;
	my($MaxYear, $MaxMon, $MaxDay, $MaxHour, $MaxMin, $MaxSec) = $EndStr =~ /^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})/;
	$MinYear -= 1900;
	$MinMon =~ s/^0//;	$MinMon --;
	$MinDay =~ s/^0//;
	$MinHour =~ s/^0//;
	$MinMin =~ s/^0//;
	$MinSec =~ s/^0//;
	$MaxYear -= 1900;
	$MaxMon =~ s/^0//;	$MaxMon --;
	$MaxDay =~ s/^0//;
	$MaxHour =~ s/^0//;
	$MaxMin =~ s/^0//;
	$MaxSec =~ s/^0//;
	my($StartTime) = timelocal($MinSec, $MinMin, $MinHour, $MinDay, $MinMon, $MinYear);
	my($EndTime) = timelocal($MaxSec, $MaxMin, $MaxHour, $MaxDay, $MaxMon, $MaxYear);
	return abs($EndTime - $StartTime);
}


# ログファイルのサイズを調べる(KB)
sub AnalyzeLogfileSize {
	my($File) = @_;
	my(@log_stat) = stat($File);
	my($log_size) = $log_stat[7];
	return $log_size;
}

sub PrintResult {
	my($Title, $ResultStr) = @_;
	my $html = &ReadTemplate("$TEMPLATEDIR/result.html");
	$html =~ s/<!--RESULT-->/$ResultStr/;
	$html =~ s/<!--TITLE-->/$Title/;
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	print "$html\n";
	exit;
}


sub MakeGraph {
	my($InputData, $Titles) = @_;
	my %ElementList = %$InputData;
	my($Str);
	$Str .= "<TABLE BORDER=\"0\">\n";
	$Str .= "<TR BGCOLOR=\"#3A6EA5\">";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[0]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[1]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[2]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[3]</FONT></td>";
	$Str .= "</TR>\n";
	my $Sum = 0;
	for my $key (keys %ElementList) {
		$Sum += $ElementList{$key};
	}
	my $order = 1;
	my $dsp_order = 1;
	my($rate, $GraphLength, $pre_velue);
	foreach my $key (ValueSort(\%ElementList)) {
		unless($ElementList{$key} == $pre_velue) {
			$dsp_order = $order;
			last if($dsp_order > $CONF{'ROW'});
		}
		$rate = int($ElementList{$key} * 10000 / $Sum) / 100;
		$GraphLength = int($CONF{'GRAPHMAXLENGTH'} * $rate / 100);

		$Str .= "<TR BGCOLOR=\"#EAEAEA\">\n";
		$Str .= "  <TD><CENTER>$dsp_order</CENTER></TD>\n";
		$Str .= "  <TD>$key</TD>\n";
		$Str .= "  <TD ALIGN=\"RIGHT\">$ElementList{$key}</TD>\n";
		$Str .= "  <TD class=\"size2\">";
		if($rate < 1) {
			$Str .= "";
		} else {
			$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar\.gif\" WIDTH=\"$GraphLength\" HEIGHT=\"10\">";
		}
		$Str .= " ($rate%)</TD></TR>\n";
		$pre_velue = $ElementList{$key};
		$order ++;
	}
	$Str .= "</TABLE>\n";
	return $Str;
}

sub MakeGraph2 {
	my($InputData, $Titles, $ConvList) = @_;
	my %ElementList = %$InputData;
	my($Str);
	$Str .= "<TABLE BORDER=\"0\">\n";
	$Str .= "<TR BGCOLOR=\"#3A6EA5\">";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[0]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[1]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[2]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[3]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[4]</FONT></td>";
	$Str .= "</TR>\n";
	my $Sum = 0;
	for my $key (keys %ElementList) {
		$Sum += $ElementList{$key};
	}
	my $order = 1;
	my $dsp_order = 1;
	my($rate, $GraphLength, $pre_velue);
	foreach my $key (ValueSort(\%ElementList)) {
		unless($ElementList{$key} == $pre_velue) {
			$dsp_order = $order;
			last if($dsp_order > $CONF{'ROW'});
		}
		$rate = int($ElementList{$key} * 10000 / $Sum) / 100;
		$GraphLength = int($CONF{'GRAPHMAXLENGTH'} * $rate / 100);
		$Str .= "<TR BGCOLOR=\"#EAEAEA\">\n";
		$Str .= "  <TD><CENTER>$dsp_order</CENTER></TD>\n";
		$Str .= "  <TD>$key</TD>\n";
		if($$ConvList{$key}) {
			$Str .= "  <TD>$$ConvList{$key}</TD>\n";
		} else {
			$Str .= "  <TD>&nbsp;</TD>\n";
		}
		$Str .= "  <TD ALIGN=\"RIGHT\">$ElementList{$key}</TD>\n";
		$Str .= "  <TD class=\"size2\">";
		if($rate < 1) {
			$Str .= "";
		} else {
			$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar\.gif\" WIDTH=\"$GraphLength\" HEIGHT=\"10\">";
		}
		$Str .= " ($rate%)</TD></TR>\n";
		$pre_velue = $ElementList{$key};
		$order ++;
	}
	$Str .= "</TABLE>\n";
	return $Str;
}

sub MakeGraph3 {
	my($InputData, $Titles, $Map) = @_;
	my %ElementList = %$InputData;
	my($Str);
	$Str .= "<TABLE BORDER=\"0\">\n";
	$Str .= "<TR BGCOLOR=\"#3A6EA5\">";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[0]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[1]</FONT></td>";
	$Str .= "<td CLASS=ListHeader><FONT COLOR=\"#FFFFFF\">$$Titles[2]</FONT></td>";
	$Str .= "</TR>\n";
	my $Sum = 0;
	for my $key (keys %ElementList) {
		$Sum += $ElementList{$key};
	}
	my($rate, $GraphLength);
	foreach my $key (sort {$a <=> $b} (keys %ElementList)) {
		$rate = int($ElementList{$key} * 10000 / $Sum) / 100;
		$GraphLength = int($CONF{'GRAPHMAXLENGTH'} * $rate / 100);

		$Str .= "<TR BGCOLOR=\"#EAEAEA\">\n";
		if($Map) {
			$Str .= "  <TD>$$Map[$key]</TD>\n";
		} else {
			$Str .= "  <TD>$key</TD>\n";
		}
		$Str .= "  <TD ALIGN=\"RIGHT\">$ElementList{$key}</TD>\n";
		$Str .= "  <TD class=\"size2\">";
		if($rate < 1) {
			$Str .= "";
		} else {
			$Str .= "<IMG SRC=\"$CONF{'IMAGE_URL'}/graphbar\.gif\" WIDTH=\"$GraphLength\" HEIGHT=\"10\">";
		}
		$Str .= " ($rate%)</TD></TR>\n";
	}
	$Str .= "</TABLE>\n";
	return $Str;
}


sub MakeCircleGraph {
	my($InputData) = @_;
	my(%ElementList) = %$InputData;
	my($ItemNum);
	$ItemNum = scalar keys %$InputData;
	if($ItemNum > 10) {
		$ItemNum = 10;
	}
	my $Str;

	if($CONF{'CIRCLE_GLAPH'}) {
		$Str .= "<APPLET\n";
		$Str .= "  CODEBASE = \"$CONF{'IMAGE_URL'}\"\n";
		$Str .= "  CODE     = \"CircleGraph.class\"\n";
		$Str .= "  NAME     = \"CircleGraph\"\n";
		$Str .= "  WIDTH    = 400\n";
		$Str .= "  HEIGHT   = 220\n";
		$Str .= "  HSPACE   = 0\n";
		$Str .= "  VSPACE   = 0\n";
		$Str .= "  ALIGN    = top\n";
		$Str .= ">\n";
		$Str .= "<PARAM NAME = \"ItemNum\" VALUE = \"$ItemNum\">\n";
		my $key;
		my $i = 1;
		my $OtherCnt = 0;
		foreach $key (ValueSort(\%ElementList)) {
			if($i < 10) {
	    		$Str .= "<PARAM NAME = \"Name$i\" VALUE = \"$key\">\n";
	    		$Str .= "<PARAM NAME = \"Value$i\" VALUE = \"$ElementList{$key}\">\n";
			} else {
				$OtherCnt += $ElementList{$key};
			}
			$i ++;
		}
		if($OtherCnt) {
			$Str .= "<PARAM NAME = \"Name10\" VALUE = \"その他\">\n";
			$Str .= "<PARAM NAME = \"Value10\" VALUE = \"$OtherCnt\">\n";
		}
		$Str .= "</APPLET>\n";
	} else {
		my $key;
		my $i = 1;
		my $OtherCnt = 0;
		my $list;
		foreach $key (ValueSort(\%ElementList)) {
			if($i < 10) {
				my $enc_name = &URL_Encode($key);
				$list .= "name$i=$enc_name&";
				$list .= "value$i=$ElementList{$key}&";
			} else {
				$OtherCnt += $ElementList{$key};
			}
			$i ++;
		}
		if($OtherCnt) {
			my $key = 'その他';
			my $enc_name = &URL_Encode($key);
			$list .= "name10=$enc_name&value10=$OtherCnt";
		} else {
			$list =~ s/\&$//;
		}
		$Str .= "<OBJECT classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\"\n";
		$Str .= "  codebase=\"http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=5,0,0,0\"\n";
		$Str .= "  WIDTH=400 HEIGHT=220>\n";
		$Str .= "  <PARAM NAME=movie VALUE=\"$CONF{'IMAGE_URL'}/CircleGraph.swf?$list\">\n";
		$Str .= "  <PARAM NAME=quality VALUE=high>\n";
		$Str .= "  <PARAM NAME=bgcolor VALUE=#FFFFFF>\n";
		$Str .= "  <EMBED\n";
		$Str .= "    src=\"$CONF{'IMAGE_URL'}/CircleGraph.swf?$list\"\n";
		$Str .= "    quality=high bgcolor=#FFFFFF\n";
		$Str .= "    WIDTH=400 HEIGHT=220\n";
		$Str .= "    TYPE=\"application/x-shockwave-flash\"\n";
		$Str .= "    PLUGINSPAGE=\"http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash\">\n";
		$Str .= "  </EMBED>\n";
		$Str .= "'</OBJECT>\n";
	}
	return $Str;
}


# URLエンコードされた文字列を、デコードして返す
sub URL_Decode {
	my($string) = @_;
	$string =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/eg;
	$string =~ s/\+/ /g;
	return $string;
}

sub URL_Encode {
	my($string) = @_;
	$string =~ s/ /+/g;
	$string =~ s/([^A-Za-z0-9\+])/'%'.unpack("H2", $1)/ego;
	return $string;
}

# 西暦、月、日を引数に取り、曜日コードを返す。
# 日:0, 月:1, 火:2, 水:3, 木:4, 金:5, 土:6
sub Youbi {
	my($year, $month, $day) = @_;
	$month =~ s/^0//;
	if($month eq '') {return '';}
	$day =~ s/^0//;
	my($time) = timelocal(0, 0, 0, $day, $month - 1, $year);
	my(@date_array) = localtime($time);
	return $date_array[6];
}

# 西暦と月を引数に取り、該当月の最終日を返す
sub LastDay {
	my($year, $month) = @_;
	$month =~ s/^0//;
	if($month =~ /[^0-9]/ || $year =~ /[^0-9]/) {
		return '';
	}
	if($month < 1 && $month > 12) {
		return '';
	}
	if($year > 2037 || $year < 1900) {
		return '';
	}
	my($lastday) = 1;
	my($time) = timelocal(0, 0, 0, 1, $month-1, $year-1900);
	my(@date_array) = localtime($time);
	my($mon) = $date_array[4];
	my($flag) = 1;
	my($count) = 0;
	while($flag) {
		if($mon ne $date_array[4]) {
			return $lastday;
			$flag = 0;
		}
		$lastday = $date_array[3];
		$time = $time + (60 * 60 * 24);
		@date_array = localtime($time);
		$count ++;
		last if($count > 40);
	}
}

sub SecureHtml {
	my($html) = @_;
	$html =~ s/\&amp;/\&/g;
	$html =~ s/\&/&amp;/g;
	$html =~ s/\"/&quot;/g;
	$html =~ s/</&lt;/g;
	$html =~ s/>/&gt;/g;
	return $html;
}

sub HtmlHeader {
	if($CONF{'AUTHFLAG'}) {
		print "P3P: CP=\"NOI TAIa\"\n";
		my $CookieHeaderString = &SetCookie('PASS', $CONF{'PASSWORD'});
		print "$CookieHeaderString\n";
	}
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	print "\n";
}

sub ErrorPrint {
	my($message) = @_;
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	print "<center>\n";
	print "$message\n";
	print "</center>\n";
	exit;
}


# 連想配列を値（value）でソートした連想配列を返す
sub ValueSort {
	my $x = shift;
	my %array=%$x;
	return sort {$array{$b} <=> $array{$a};} keys %array;
}

# 指定された定義ファイルを読み取り、連想配列を返す。
sub ReadDef {
	my($file) = @_;
	my(@buff, %array);
	open(FILE, "$file") || &ErrorPrint("$file をオープンできませんでした。");
	while(<FILE>) {
		if(/^\s*\#/) {next;}
		chop;
		@buff = split(/=/);
		if($buff[0] && $buff[1]) {
			$array{$buff[0]} = $buff[1];
		} else {
			next;
		}
	}
	close(FILE);
	return %array;
}

sub ReadTitleDat {
	my $file = './data/title.dat';
	my(@buff, %array);
	open(FILE, "$file") || &ErrorPrint("$file をオープンできませんでした。");
	while(my $line=<FILE>) {
		if($line =~ /^\s*\#/) {next;}
		chop $line;
		if($line =~ /^([^\t]+)\t+(.+)$/) {
			$array{$1} = $2;
		} elsif($line =~ /^([^\=]+)\=(.+)$/) {
			$array{$1} = $2;
		} else {
			next;
		}
	}
	close(FILE);
	return %array;
}

sub PrintAuthForm {
	my($Repeat) = @_;
	my $html = &ReadTemplate("$TEMPLATEDIR/logon.html");
	my $form;
	if($Repeat) {
		$form .= "<font color=\"\#FF0000\">パスワードが違います。</font>\n";
	}
	$form .= $q->br;
	$form .= $q->start_form(-method=>'POST',-action=>$CGI_URL);
	$form .= "パスワード ";
	$form .= $q->password_field(-name=>'PASS');
	$form .= $q->submit(-name=>'submit', -value=>'　認　証　');
	$html =~ s/<!--FORM-->/$form/;
	$html =~ s/<!--COPYRIGHT-->/$COPYRIGHT/g;
	$html =~ s/<!--COPYRIGHT4-->/$COPYRIGHT4/g;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "$html\n";
	exit;
}

sub SetCookie {
	my($CookieName, $CookieValue) = @_;
	# URLエンコード
	$CookieValue =~ s/([^\w\=\& ])/'%' . unpack("H2", $1)/eg;
	$CookieValue =~ tr/ /+/;
	my($CookieHeaderString) = "Set-Cookie: $CookieName=$CookieValue\;";
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


#指定したURL(URI)から、HTMLタイトルを取得する。
sub GetHtmlTitle {
	my($URL) = @_;
	my($Title, $Path);
	my $HtmlFile;
	if($CONF{'URL2PATH_FLAG'}) {
		my($key);
		for $key (keys %URL2PATH) {
			if($URL =~ /^$key/) {
				$HtmlFile = $URL;
				$HtmlFile =~ s/^$key/$URL2PATH{$key}/;
			}
		}
		unless($HtmlFile) {
			return '';
		}
	} else {
		$_ = $URL;
		m|https*://[^/]+/(.*)|;
		$Path = '/'.$1;
		$HtmlFile = $ENV{'DOCUMENT_ROOT'}.$Path;
	}
	$HtmlFile =~ s/\?.*$//;
	$HtmlFile =~ s/\#.*$//;
	unless(-e $HtmlFile) {return ''};
	my $size = -s $HtmlFile;
	if(!open(HTML, "$HtmlFile")) {
		return '';
	}
	binmode(HTML);	# For Windows
	my $buf;
	sysread(HTML, $buf, $size);
	close(HTML);
	if( $buf =~ /<title>([^<]*)<\/title>/i ) {
		$Title = $1;
	}
	if($Title) {
		if($JFLAG) {
			eval {
				&Jcode::convert(\$Title, "sjis");
			}
		} else {
			eval {
				&jcode::convert(\$Title, "sjis");
			}
		}
		return $Title;
	} else {
		return '';
	}
}


sub GetLogDateList {
	my($LogFile) = @_;
	my @DateList = ();
	if(-e $LogFile) {
		open(LOGFILE, "$LogFile") || return @DateList;
	} else {
		return @DateList;
	}
	my($Buff, $DateBuff, %DateListBuff);
	while(<LOGFILE>) {
		chop;
		next if($_ eq '');
		($Buff) = split(/\s/);
		unless($Buff) {next;}
		$DateBuff = substr($Buff, 0, 8);
		$DateListBuff{$DateBuff} ++;
	}
	close(LOGFILE);
	my $key;
	for $key (sort keys %DateListBuff) {
		if($key =~ /^[0-9]{8}$/) {
			push(@DateList, $key);
		}
	}
	return @DateList;
}


sub GetLastMonth {
	my($ThisYearMonth) = @_;
	my $ThisYear = substr($ThisYearMonth, 0, 4);
	my $ThisMonth = substr($ThisYearMonth, 4, 2);
	$ThisMonth =~ s/^0//;
	my($LastMonth, $LastYear);
	if($ThisMonth == 1) {
		$LastMonth = 12;
		$LastYear = $ThisYear - 1;
	} else {
		$LastMonth = $ThisMonth - 1;
		$LastYear = $ThisYear;
	}
	if($LastMonth < 10) {
		$LastMonth = "0$LastMonth";
	}
	return "$LastYear$LastMonth";
}


sub GetNextMonth {
	my($ThisYearMonth) = @_;
	my $ThisYear = substr($ThisYearMonth, 0, 4);
	my $ThisMonth = substr($ThisYearMonth, 4, 2);
	$ThisMonth =~ s/^0//;
	my($NextMonth, $NextYear);
	if($ThisMonth == 12) {
		$NextMonth = 1;
		$NextYear = $ThisYear + 1;
	} else {
		$NextMonth = $ThisMonth + 1;
		$NextYear = $ThisYear;
	}
	if($NextMonth < 10) {
		$NextMonth = "0$NextMonth";
	}
	return "$NextYear$NextMonth";
}


sub GetPrefKeyword {
	my($HostName) = @_;
	my (@HostParts, @TmpList);
	my $key = '';
	@HostParts = split(/\./, $HostName);
	if($HostName =~ /\.alpha-net\.ne\.jp$/) {
		@TmpList = split(/\-/, $HostName);
		if($TmpList[0] =~ /^fl/) {
			$_ = $TmpList[1];
		} else {
			$_ = $TmpList[0];
		}
		m/^([a-zA-Z]+)/;
		$key = $1;
	} elsif($HostName =~ /\.att\.ne\.jp$/) {
		$key = $HostParts[2];
		$key =~ s/^ipc//;
		$key =~ s/^dsl//;
		$key =~ s/[0-9]+$//;
	} elsif($HostName =~ /\.coara\.or\.jp$/) {
		@TmpList = split(/\-/, $HostParts[0]);
		$key = $TmpList[0];
		$key =~ s/[0-9]+$//;
		$key =~ s/ap$//;
	} elsif($HostName =~ /\.dion\.ne\.jp$/) {
		$key = $HostParts[0];
		$key =~ s/[0-9\-]+//;
	} elsif($HostName =~ /\.dti\.ne\.jp$/) {
		@TmpList = split(/\-/, $HostParts[1]);
		$key = $TmpList[0];
	} elsif($HostName =~ /\.hi-ho\.ne\.jp$/) {
		@TmpList = split(/\-/, $HostParts[0]);
		$key = $TmpList[0];
		$key =~ s/^(adsl|ea|ip)//;
		$key =~ s/[0-9]+$//;
	} elsif($HostName =~ /\.highway\.ne\.jp$/) {
		$key = $HostParts[1];
		$key =~ s/^ip\-//;
		$key =~ s/^e\-//;
	} elsif($HostName =~ /\.interq\.or\.jp$/) {
		@TmpList = split(/\-/, $HostParts[0]);
		$key = $TmpList[0];
		$key =~ s/ipconnect$//;
		$key =~ s/[0-9]+$//;
	} elsif($HostName =~ /\.mbn\.or\.jp$/) {
		$key = $HostParts[1];
	} elsif($HostName =~ /\.mesh\.ad\.jp$/) {
		$key = $HostParts[1];
		$key =~ s/[0-9]+$//;
	} elsif($HostName =~ /\.psinet.ne.jp$/) {
		$key = $HostParts[1];
		$key =~ s/^fli\-//;
	} elsif($HostName =~ /\.sannet\.ne\.jp$/) {
		$key = $HostParts[1];
	} elsif($HostName =~ /\.uu\.net$/) {
		$key = $HostParts[2];
		$key =~ s/[0-9]+$//;
	} elsif($HostName =~ /\.ocn\.ne\.jp$/) {
		$key = $HostParts[1];
	} elsif($HostName =~ /\.zero\.ad\.jp$/) {
		@TmpList = split(/\-/, $HostParts[0]);
		if($TmpList[0] eq 'f') {
			$key = $TmpList[1];
		} else {
			$key = $TmpList[0];
		}
		$key =~ s/[0-9]+$//;
	} elsif($HostName =~ /\.so-net\.ne\.jp$/) {
		if($HostParts[1] =~ /^ntt/) {
			$key = substr($HostParts[1], 3, 4);
		} else {
			$key = substr($HostParts[1], 0, 4);
		}
	} elsif($HostName =~ /\.infoweb\.ne\.jp$/) {
		if($HostParts[0] =~ /^nttkyo/) {
			$key = 'tkyo';
		} elsif($HostParts[0] =~ /^ntt([a-z]{4})/) {
			$key = $1;
		} elsif($HostParts[0] =~ /^(ea|ac|nt|ho|ct|st|th|ht|tc)([a-z]{4})/) {
			$key = $2;
		} elsif($HostParts[0] =~ /^([a-z]+)/) {
			$key = $1;
		}
	} elsif($HostName =~ /\.pias\.ne\.jp$/) {
		$_ = $HostParts[0];
		m/^([a-zA-Z]+)/;
		$key = $1;
	} elsif($HostName =~ /\.nttpc\.ne\.jp$/) {
		$key = $HostParts[2];
	} elsif($HostName =~ /\.interlink\.or\.jp$/) {
		$key = $HostParts[1];
	} elsif($HostName =~ /\.kcom\.ne\.jp$/) {
		$key = $HostParts[1];
		$key =~ s/[0-9\-]+$//;
	} elsif($HostName =~ /\.home\.ne\.jp$/) {
		$key = $HostParts[1];
		$key =~ s/[0-9]+$//;
	} elsif($HostName =~ /\.isao\.net$/) {
		$key = $HostParts[1];
		$key =~ s/[0-9]+$//;
	} else {
		my(@AreaList) = ('hokkaido', 'aomori', 'iwate', 'miyagi', 'akita', 'yamagata', 'fukushima',
	                 'ibaraki', 'tochigi', 'gunma', 'saitama', 'chiba', 'tokyo', 'kanagawa',
	                 'niigata', 'toyama', 'ishikawa', 'fukui', 'yamanashi', 'nagano', 'gifu',
	                 'shizuoka', 'aichi', 'mie', 'shiga', 'kyoto', 'osaka', 'hyogo', 'nara',
	                 'wakayama', 'tottori', 'shimane', 'okayama', 'hiroshima', 'yamaguchi',
	                 'tokushima', 'kagawa', 'ehime', 'kochi', 'fukuoka', 'saga', 'nagasaki',
	                 'kumamoto', 'oita', 'miyazaki', 'kagoshima', 'okinawa', 'sapporo',
	                 'sendai', 'chiba', 'yokohama', 'kawasaki', 'nagoya', 'kyoto', 'osaka',
	                 'kobe', 'hiroshima', 'fukuoka', 'kitakyushu');
		my $tld = pop @HostParts;
		my $sld = pop @HostParts;
		if($tld eq 'jp' and grep(/^$sld$/, @AreaList)) {
			$key = $sld;
		}
	}
	return $key;
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
	$html =~ s/<!--COPYRIGHT-->/$COPYRIGHT/;
	$html =~ s/<!--COPYRIGHT2-->/$COPYRIGHT2/g;
	$html =~ s/<!--COPYRIGHT3-->/$COPYRIGHT3/g;
	$html =~ s/<!--COPYRIGHT4-->/$COPYRIGHT4/g;
	return $html;
}

sub CheckHoliday {
	my($year, $mon, $day) = @_;
	#指定日が存在する日かをチェックする
	my $time;
	eval {$time = timelocal(0, 0, 0, $day, $mon-1, $year-1900);};
	if($@) {return -1;}
	#当日を特定する。
	my @list = localtime($time);
	my $today = sprintf("%02d", $mon).sprintf("%02d", $day);
	my $youbi = $list[6];
	my $order = int(($day-1) / 7) + 1;
	#前日を特定する。
	my @y_list = localtime($time-60*60*24);
	my $yesterday = sprintf("%02d", $y_list[4]+1).sprintf("%02d", $y_list[3]);
	my $y_youbi = $y_list[6];
	my $y_order = int(($y_list[3] - 1) / 7) + 1;
	my $y_flag = 0;
	#翌日を特定する
	my @t_list = localtime($time+60*60*24);
	my $tomorrow = sprintf("%02d", $t_list[4]+1).sprintf("%02d", $t_list[3]);
	my $t_youbi = $t_list[6];
	my $t_order = int(($t_list[3] - 1) / 7) + 1;
	my $t_flag = 0;

	#当日が日曜日かどうかをチェック
	#日曜日であれば、無条件で1を返す。
	if($youbi == 0) {return 1;}

	#日付が決まっている祝日を定義
	my @fix_horidays = (
		'0101',		#元日
		'0211',		#建国記念日
		'0429',		#みどりの日
		'0503',		#憲法記念日
		'0505',		#こどもの日
		'1103',		#文化の日
		'1123',		#勤労感謝の日
	);
	#春分の日と秋分の日を挿入する。
	#毎年変更になるので、適宜修正が必要。
	if($year eq '2003') {
		push(@fix_horidays, '0321', '0923');
	} elsif($year eq '2004') {
		push(@fix_horidays, '0320', '0923');
	}
	#1989年（平成元年）以降であれば、天皇誕生日を挿入する。
	if($year >= 1989) {
		push(@fix_horidays, '1223');
	}

	#当日が固定祝日かどうかをチェック
	#固定祝日であれば、1を返す。
	if(grep(/^$today$/, @fix_horidays)) {return 1;}

	#当日が変動祝日かどうかをチェック
	#  成人の日 １月の第２月曜日
	if($mon eq '1' && $youbi == 1 && $order == 2) {return 1;}
	#  海 の 日 ７月の第３月曜日
	if($mon eq '7' && $youbi == 1 && $order == 3) {return 1;}
	#  敬老の日 ９月の第３月曜日
	if($mon eq '9' && $youbi == 1 && $order == 3) {return 1;}
	#  体育の日 １０月の第２月曜日
	if($mon eq '10' && $youbi == 1 && $order == 2) {return 1;}

	#昨日が固定祝日かどうかをチェック
	if(grep(/^$yesterday$/, @fix_horidays)) {$y_flag = 1;}
	#昨日が変動祝日かどうかをチェック
	my $y_mon = substr($yesterday, 0, 2);
	if($y_mon eq '01' && $y_youbi == 1 && $y_order == 2) {$y_flag = 1;}
	if($y_mon eq '07' && $y_youbi == 1 && $y_order == 3) {$y_flag = 1;}
	if($y_mon eq '09' && $y_youbi == 1 && $y_order == 3) {$y_flag = 1;}
	if($y_mon eq '10' && $y_youbi == 1 && $y_order == 2) {$y_flag = 1;}
	#昨日が祝日で、かつ日曜日の場合には、当日は休日
	if($y_flag == 1 && $y_youbi == 0) {return 1;}

	#明日が固定祝日かどうかをチェック
	if(grep(/^$tomorrow$/, @fix_horidays)) {$t_flag = 1;}
	#明日が変動祝日かどうかをチェック
	my $t_mon = substr($tomorrow, 0, 2);
	if($t_mon eq '01' && $t_youbi == 1 && $t_order == 2) {$t_flag = 1;}
	if($t_mon eq '07' && $t_youbi == 1 && $t_order == 3) {$t_flag = 1;}
	if($t_mon eq '09' && $t_youbi == 1 && $t_order == 3) {$t_flag = 1;}
	if($t_mon eq '10' && $t_youbi == 1 && $t_order == 2) {$t_flag = 1;}

	#昨日と明日がともに祝日の場合には、当日は休日。
	if($y_flag && $t_flag) {return 1;}

	#以上のチェックにひっかからなかったら、休日でない。
	return 0;
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

sub Auth {
	my %cookies = &GetCookie;
	my $inpass = $q->param('PASS');
	if($inpass eq '') {
		$inpass = $cookies{'PASS'};
	}
	if($inpass) {
		if($inpass ne $CONF{'PASSWORD'}) {
			&PrintAuthForm(1);
		}
	} else {
		&PrintAuthForm();
	}
}

sub SpecifyLogFileName {
	my $filename = $q->param('LOG');
	unless($filename) {
		my $date_str = &GetToday;
		my $mon_str = substr($date_str, 0, 6) . '00';
		if($CONF{'LOTATION'} == 2) {	#日ごとのローテーション
			$filename = "$PRE_LOGNAME\.$date_str\.cgi";
		} elsif($CONF{'LOTATION'} == 3) {	#月ごとのローテーション
			$filename = "$PRE_LOGNAME\.$mon_str\.cgi";
		} elsif($CONF{'LOTATION'} == 4) {	#週ごとのローテーション
			my $t = time + $CONF{'TIMEDIFF'}*60*60;
			my @date_array = localtime($t);
			my $wday = $date_array[6];
			my $epoc_time = $t;
			$epoc_time -= $wday*60*60*24;
			@date_array = localtime($epoc_time);
			my $day = $date_array[3];
			if($day < 10) {$day = "0$day";}
			my $mon = $date_array[4];
			$mon ++;	if($mon < 10) {$mon = "0$mon";}
			my $year = $date_array[5];
			$year += 1900;
			$filename = "$PRE_LOGNAME\.$year$mon$day\.cgi";
		} else {
			$filename = "$PRE_LOGNAME\.cgi";
		}
	}
	return $filename
}

sub RedirectPage {
	my($url) = @_;
	print $q->header(-type=>'text/html; charset=Shift_JIS');
	print "<html><head><title>$COPYRIGHT</title>";
	print "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"0; URL=$url\">";
	print "</head><body>\n";
	print "自動的に転送します。転送しない場合には<a href=\"$url\">こちら</a>をクリックして下さい。\n";
	print "</body></html>\n";
	exit;
}

sub User_Agent {
	my($user_agent, $remote_host) = @_;
	my($platform, @agentPart, $browser, $browser_v);
	my($platform_v, @agentPart2, $user_agent2, @buff, @buff2, @buff3);
	my($flag, $key, @version_buff);

	if($user_agent =~ /DoCoMo/i) {
		$platform = 'DoCoMo';
		@agentPart = split(/\//, $user_agent);
		$browser = 'DoCoMo';
		$browser_v = $agentPart[1];
		$platform_v = $agentPart[2];
		if($platform_v eq '') {
			if($user_agent =~ /DoCoMo\/([0-9\.]+)\s+([0-9a-zA-Z]+)/) {
				$browser_v = $1;
				$platform_v = $2;
			}
		}
	} elsif($user_agent =~ /NetPositive/i) {
		$browser = 'NetPositive';
		if($user_agent =~ /NetPositive\/([0-9\.\-]+)/) {
			$browser_v = $1;
		}
		$platform = 'BeOS';
		$platform_v = '';
	} elsif($user_agent =~ /OmniWeb/) {
		$browser = 'OmniWeb';
		if($user_agent =~ /Mac_PowerPC/i) {
			$platform = 'MacOS';
			$platform_v = 'PowerPC';
		} else {
			$platform = '';
			$platform_v = '';
		}
		if($user_agent =~ /OmniWeb\/([0-9\.]+)/) {
			$browser_v = $1;
		} else {
			$browser_v = '';
		}
	} elsif($user_agent =~ /Cuam/i) {
		$browser = 'Cuam';
		$platform = 'Windows';
		$browser_v = '';
		$platform_v = '';
		if($user_agent =~ /Cuam Ver([0-9\.]+)/i) {
			$platform_v = '';
			$browser_v = $1;
		} else {
			if($user_agent =~ /Windows\s+([^\;\)]+)/) {
				$platform_v = $1;
			}
			if($user_agent =~ /Cuam\s+(0-9a-z\.)/) {
				$browser_v = $1;
			}
		}
	} elsif($user_agent =~ /^JustView\/([0-9\.]+)/) {
		$platform = 'Windows';
		$platform_v = '';
		$browser = 'JustView';
		$browser_v = $1;
	} elsif($user_agent =~ /^sharp pda browser\/([0-9\.]+).*\((.+)\//) {
		$platform = 'ZAURUS';
		$platform_v = $2;
		$browser = 'sharp_pda_browser';
		$browser_v = $1;
	} elsif($user_agent =~ /DreamPassport\/([0-9\.]+)/) {
		$platform = 'Dreamcast';
		$platform_v = '';
		$browser = 'DreamPassport';
		$browser_v = $1;
	} elsif($user_agent =~ /^Sonybrowser2 \(.+\/PlayStation2 .+\)/) {
		$platform = 'PlayStation2';
		$platform_v = '';
		$browser = 'Sonybrowser2';
		$browser_v = '';
	} elsif($user_agent =~ /(CBBoard|CBBstandard)\-[0-9\.]+/) {
		$platform = 'DoCoMo';
		$platform_v = 'ColorBrowserBorad';
		$browser = 'DoCoMo';
		$browser_v = 'ColorBrowserBorad';
	} elsif($user_agent =~ /^PDXGW/) {
		$platform = 'DDI POCKET';
		$platform_v = 'H"';
		$browser = 'DDI POCKET';
		$browser_v = 'H"';
	} elsif($user_agent =~ /^Sleipnir Version ([0-9\.]+)/) {
		$browser = 'Sleipnir';
		$browser_v = $1;
		$platform = 'Windows';
		$platform_v = '';
	} elsif($user_agent =~ /Safari\/([0-9]+)/) {
		$browser = 'Safari';
		$browser_v = $1;
		$platform = 'MacOS';
		if($user_agent =~ / PPC /) {
			$platform_v = 'PowerPC';
		}
	} elsif($user_agent =~ /UP\.\s*Browser/i) {
		$user_agent =~ s/UP\.\s*Browser/UP\.Browser/;
		$browser = 'UP.Browser';
		@agentPart = split(/ /, $user_agent);
		if($agentPart[0] =~ /KDDI/i) {
			my @tmp = split(/\-/, $agentPart[0]);
			$platform_v = $tmp[1];
			my @tmp2 = split(/\//, $agentPart[1]);
			$browser_v = $tmp2[1];
		} else {
			@agentPart2 = split(/\//, $agentPart[0]);
			($browser_v, $platform_v) = split(/\-/, $agentPart2[1]);
		}
		my %devid_list = (
			'P-PAT'=>'DoCoMo,P-PAT',
			'D2'=>'DoCoMo,D2',
			'TS24'=>'au,A5304T',
			'HI23'=>'au,A5303H',
			'CA22'=>'au,A5302CA',
			'TS23'=>'au,A5301T',
			'TS21'=>'au,C5001T',
			'SA22'=>'au,A3015SA',
			'SN21'=>'au,A3014S',
			'TS22'=>'au,A3013T',
			'CA21'=>'au,A3012CA',
			'SA21'=>'au,A3011SA',
			'MA21'=>'au,C3003P',
			'KC21'=>'au,C3002K',
			'HI21'=>'au,C3001H',
			'SA24'=>'au,A1302SA',
			'SN23'=>'au,A1301S',
			'SN22'=>'au,A1101S',
			'ST14'=>'au,A1014ST',
			'KC15'=>'au,A1013K',
			'KC14'=>'au,A1012K',
			'ST13'=>'au,A1011ST',
			'SN17'=>'au,C1002S',
			'SY15'=>'au,C1001SA',
			'CA14'=>'au,C452CA',
			'HI14'=>'au,C451H',
			'TS14'=>'au,C415T',
			'KC13'=>'au,C414K',
			'SN15'=>'au,C413S',
			'SN16'=>'au,C413S',
			'SY14'=>'au,C412SA',
			'ST12'=>'au,C411ST',
			'TS13'=>'au,C410T',
			'CA13'=>'au,C409CA',
			'MA13'=>'au,C408P',
			'HI13'=>'au,C407H',
			'SN13'=>'au,C406S',
			'SY13'=>'au,C405SA',
			'SN12'=>'au,C404S',
			'SN14'=>'au,C404S',
			'ST11'=>'au,C403ST',
			'DN11'=>'au,C402DE',
			'SY12'=>'au,C401SA',
			'KC12'=>'au,C313K',
			'CA12'=>'au,C311CA',
			'TS12'=>'au,C310T',
			'HI12'=>'au,C309H',
			'MA11'=>'au,C308P',
			'MA12'=>'au,C308P',
			'KC11'=>'au,C307K',
			'SN11'=>'au,C305S',
			'SY11'=>'au,C304SA',
			'CA11'=>'au,C303CA',
			'HI11'=>'au,C302H',
			'TS11'=>'au,C301T',
			'DN01'=>'au,C202DE',
			'HI01'=>'au,C201H',
			'HI02'=>'au,C201H',
			'SNC1'=>'au,D306S',
			'SNI1'=>'au,705G',
			'MAC1'=>'au,D305P',
			'MAI1 '=>'au,704G',
			'MAC2'=>'au,D305P',
			'MAI2'=>'au,704G',
			'KCC2'=>'au,D304K',
			'KCI2'=>'au,703G',
			'KCC1'=>'au,D303K',
			'KCI1'=>'au,702G',
			'TSC1'=>'au,D302T',
			'TSI1'=>'au,701G',
			'SYC1'=>'au,D301SA',
			'TS31'=>'TU-KA,SYT4',
			'KCTB'=>'TU-KA,TK23',
			'KCTA'=>'TU-KA,TK22',
			'TST6'=>'TU-KA,TT22',
			'KCT9'=>'TU-KA,TK21',
			'TST5'=>'TU-KA,TT21',
			'TST4'=>'TU-KA,TT11',
			'TST3'=>'TU-KA,TT03',
			'TST2'=>'TU-KA,TT02',
			'TST1'=>'TU-KA,TT01',
			'KCT6'=>'TU-KA,TK05',
			'KCT5'=>'TU-KA,TK04',
			'KCT4'=>'TU-KA,TK03',
			'KCT2'=>'TU-KA,TK02',
			'KCT3'=>'TU-KA,TK02',
			'KCT1'=>'TU-KA,TK01',
			'SYT2'=>'TU-KA,TS02',
			'SYT1'=>'TU-KA,TS01',
			'KCT8'=>'TU-KA,TK12',
			'KCT7'=>'TU-KA,TK11',
			'MIT1'=>'TU-KA,TD11',
			'MAT3'=>'TU-KA,TP11',
			'SYT3'=>'TU-KA,TS11',
			'MAT1'=>'TU-KA,TP01',
			'MAT2'=>'TU-KA,TP01',
			'TST4'=>'TU-KA,TT11',
			'NT95'=>'UP.SDK',
			'UPG'=>'UP.SDK'
		);
		if($devid_list{$platform_v} eq '') {
			$platform = '';
			$platform_v = '';
		} else {
			($platform, $platform_v) = split(/,/, $devid_list{$platform_v});
		}
	} elsif($user_agent =~ /^J-PHONE/) {
		$platform = 'J-PHONE';
		$browser = 'J-PHONE';
		my @parts = split(/\//, $user_agent);
		$browser_v = $parts[1];
		$platform_v = $parts[2];
	} elsif($user_agent =~ /^ASTEL\/(.+)\/(.+)\/(.+)\//) {
		$platform = 'ASTEL';
		$browser = 'ASTEL';
		$browser_v = '';
		$platform_v = substr($2, 0, 5);
	} elsif($user_agent =~ /^Mozilla\/.+ AVE-Front\/(.+) \(.+\;Product=(.+)\;.+\)/) {
		$browser = 'NetFront';
		$browser_v = $1;
		$platform = $2;
		$platform_v = '';
	} elsif($user_agent =~ /^Mozilla\/.+ Foliage-iBrowser\/([0-9\.]+) \(WinCE\)/) {
		$platform = 'Windows';
		$platform_v = 'CE';
		$browser = 'Foliage-iBrowser';
		$browser_v = $1;		
	} elsif($user_agent =~ /^Mozilla\/.+\(compatible\; MSPIE ([0-9\.]+)\; Windows CE/) {
		$platform = 'Windows';
		$platform_v = 'CE';
		$browser = 'PocketIE';
		$browser_v = $1;
	} elsif($user_agent =~ /Opera/) {
		$browser = "Opera";
		if($user_agent =~ /^Opera\/([0-9\.]+)/) {
			$browser_v = $1;
		} elsif($user_agent =~ /Opera\s+([0-9\.]+)/) {
			$browser_v = $1;
		} else {
			$browser_v = '';
		}
		if($user_agent =~ /Windows\s+([^\;]+)(\;|\))/i) {
			$platform = "Windows";
			$platform_v = $1;
			if($platform_v eq 'NT 5.0') {
				$platform_v = '2000';
			} elsif($platform_v eq 'NT 5.1') {
				$platform_v = 'XP';
			} elsif($platform_v eq 'ME') {
				$platform_v = 'Me';
			}
		} elsif($user_agent =~ /Macintosh\;[^\;]+\;([^\)]+)\)/) {
			$platform = "MacOS";
			$platform_v = $1;
			if($platform_v eq 'PPC') {
				$platform_v = 'PowerPC';
			}
		} elsif($user_agent =~ /Mac_PowerPC/i) {
			$platform = 'MacOS';
			$platform_v = 'PowerPC';
		} elsif($user_agent =~ /Linux\s+([0-9\.\-]+)/) {
			$platform = "Linux";
			$platform_v = $1;
		} elsif($user_agent =~ /BeOS ([A-Z0-9\.\-]+)(\;|\))/) {
			$platform = 'BeOS';
			$platform_v = $1;
		} else {
			$platform = '';
			$platform_v = '';
		}
	} elsif($user_agent =~ /^Mozilla\/[^\(]+\(compatible\; MSIE .+\)/) {
		if($user_agent =~ /NetCaptor ([0-9\.]+)/) {
			$browser = 'NetCaptor';
			$browser_v = $1;
		} else {
			$browser = 'InternetExplorer';
			$user_agent2 = $user_agent;
			$user_agent2 =~ s/ //g;
			@buff = split(/\;/, $user_agent2);
			@version_buff = grep(/MSIE/i, @buff);
			$browser_v = $version_buff[0];
			$browser_v =~ s/MSIE//g;
			if($browser_v =~ /^([0-9]+)\.([0-9]+)/) {
        			$browser_v = "$1\.$2";
			}
		}

		if($user_agent =~ /Windows 3\.1/i) {
			$platform = 'Windows';
			$platform_v = '3.1';
		} elsif($user_agent =~ /Win32/i) {
			$platform = 'Windows';
			$platform_v = '32';
		} elsif($user_agent =~ /Windows 95/i) {
			$platform = 'Windows';
			$platform_v = '95';
		} elsif($user_agent =~ /Windows 98/i) {
			$platform = 'Windows';
			if($user_agent =~ /Win 9x 4\.90/) {
				$platform_v = 'Me';
			} else {
				$platform_v = '98';
			}
		} elsif($user_agent =~ /Windows NT 5\.0/i) {
			$platform = 'Windows';
			$platform_v = '2000';
		} elsif($user_agent =~ /Windows NT 5\.1/i) {
			$platform = 'Windows';
			$platform_v = 'XP';
		} elsif($user_agent =~ /Windows NT/i 
				&& $user_agent !~ /Windows NT 5\.0/i) {
			$platform = 'Windows';
			$platform_v = 'NT';
		} elsif($user_agent =~ /Windows 2000/) {
			$platform = 'Windows';
			$platform_v = '2000';
		} elsif($user_agent =~ /Windows ME/i) {
			$platform = 'Windows';
			$platform_v = 'Me';
		} elsif($user_agent =~ /Windows XP/i) {
			$platform = 'Windows';
			$platform_v = 'XP';
		} elsif($user_agent =~ /Windows CE/i) {
			$platform = 'Windows';
			$platform_v = 'CE';
		} elsif($user_agent =~ /Mac/i) {
			$platform = 'MacOS';
			if($user_agent =~ /Mac_68000/i) {
				$platform_v = '68K';
			} elsif($user_agent =~ /Mac_PowerPC/i) {
				$platform_v = 'PowerPC';
			}
		} elsif($user_agent =~ /WebTV/i) {
			$platform = 'WebTV';
			@buff2 = split(/ /, $user_agent);
			@buff3 = split(/\//, $buff2[1]);
			$platform_v = $buff3[1];
		} else {
			$platform = '';
			$platform_v = '';
		}
	} elsif($user_agent =~ /^Mozilla\/([0-9\.]+)/) {
		$browser = 'NetscapeNavigator';
		$browser_v = $1;
		if($user_agent =~ /Gecko\//) {
			if($user_agent =~ /Netscape[0-9]*\/([0-9a-zA-Z\.]+)/) {
				$browser_v = $1;
			} elsif($user_agent =~ /Phoenix\/([0-9a-zA-Z\.]+)/) {
				$browser = 'Phoenix';
				$browser_v = $1;
			} elsif($user_agent =~ /Chimera\/([0-9a-zA-Z\.]+)/) {
				$browser = 'Chimera';
				$browser_v = $1;
			} else {
				$browser = 'Mozilla';
				if($user_agent =~ /rv:([0-9\.]+)/) {
					$browser_v = $1;
				} else {
					$browser_v = '';
				}
			}
		}

		if($user_agent =~ /Win95/) {
			$platform = 'Windows';
			$platform_v = '95';
		} elsif($user_agent =~ /Windows 95/) {
			$platform = 'Windows';
			$platform_v = '95';
		} elsif($user_agent =~ /Win 9x 4\.90/i) {
			$platform = 'Windows';
			$platform_v = 'Me';
		} elsif($user_agent =~ /Windows Me/i) {
			$platform = 'Windows';
			$platform_v = 'Me';
		} elsif($user_agent =~ /Win98/i) {
			$platform = 'Windows';
			$platform_v = '98';
		} elsif($user_agent =~ /WinNT/i) {
			$platform = 'Windows';
			$platform_v = 'NT';
		} elsif($user_agent =~ /Windows NT 5\.0/i) {
			$platform = 'Windows';
			$platform_v = '2000';
		} elsif($user_agent =~ /Windows NT 5\.1/i) {
			$platform = 'Windows';
			$platform_v = 'XP';
		} elsif($user_agent =~ /Windows 2000/i) {
			$platform = 'Windows';
			$platform_v = '2000';
		} elsif($user_agent =~ /Windows XP/i) {
			$platform = 'Windows';
			$platform_v = 'XP';
		} elsif($user_agent =~ /Macintosh/i) {
			$platform = 'MacOS';
			if($user_agent =~ /68K/i) {
				$platform_v = '68K';
			} elsif($user_agent =~ /PPC/i) {
				$platform_v = 'PowerPC';
			}
		} elsif($user_agent =~ /SunOS/i) {
			$platform = 'SunOS';
			if($user_agent =~ /SunOS\s+([0-9\-\.]+)/i) {
				$platform_v = $1;
			} else {
				$platform_v = '';
			}
		} elsif($user_agent =~ /Linux/i) {
			$platform = 'Linux';
			if($user_agent =~ /Linux\s+([0-9\-\.]+)/) {
				$platform_v = $1;
			} else {
				$platform_v = '';
			}
		} elsif($user_agent =~ /FreeBSD/i) {
			$platform = 'FreeBSD';
			if($user_agent =~ /FreeBSD\s+([a-zA-Z0-9\.\-\_]+)/i) {
				$platform_v = $1;
			} else {
				$platform_v = '';
			}
		} elsif($user_agent =~ /NetBSD/i) {
			$platform = 'NetBSD';
			$platform_v = '';
		} elsif($user_agent =~ /AIX/i) {
			$platform = 'AIX';
			if($user_agent =~ /AIX\s+([0-9\.]+)/) {
				$platform_v = $1;
			} else {
				$platform_v = '';
			}
		} elsif($user_agent =~ /IRIX/i) {
			$platform = 'IRIX';
			if($user_agent =~ /IRIX\s+([0-9\.]+)/i) {
				$platform_v = $1;
			} else {
				$platform_v = '';
			}
		} elsif($user_agent =~ /HP-UX/i) {
			$platform = 'HP-UX';
			if($user_agent =~ /HP-UX\s+([a-zA-Z0-9\.]+)/i) {
				$platform_v = $1;
			} else {
				$platform_v = '';
			}
		} elsif($user_agent =~ /OSF1/i) {
			$platform = 'OSF1';
			if($user_agent =~ /OSF1\s+([a-zA-Z0-9\.]+)/i) {
				$platform_v = $1;
			} else {
				$platform_v = '';
			}
		} elsif($user_agent =~ /BeOS/i) {
			$platform = 'BeOS';
			$platform_v = '';
		} else {
			$platform = '';
			$platform_v = '';
		}
	} else {
		$platform = '';
		$platform_v = '';
		$browser = '';
		$browser_v = '';
	}

	return ($platform, $platform_v, $browser, $browser_v);

}


