#!/usr/bin/perl
################################################################################
# 高機能アクセス解析CGI Proffesional版（アクセスログ ロギング用）
# Ver 4.7
# Copyright(C) futomi 2001 - 2003
# http://www.futomi.com/
###############################################################################
use strict;
use Time::Local;
use CGI;
my $q = new CGI;
$| = 1;

#このCGIの設定
my $CONF_DATA = './data/config.cgi';
my $JPEG_FILE = './acclogo.jpg';
my $GIF_FILE = './acclogo.gif';
my $PNG_FILE = './acclogo.png';
my $RESTRICT_COOKIE_NAME = 'accrestrict';

#自アクセス制限対象の場合、ロギングせずに終了
my %cookie = &GetCookie;
if($cookie{$RESTRICT_COOKIE_NAME}) {
	&PrintImage;
	exit;
}

#設定を読み取る
my %CONF = &GetConf($CONF_DATA);
my $LOTATION = $CONF{'LOTATION'};
my @REJECT_HOSTS = split(/,/, $CONF{'REJECT_HOSTS'});
my $USECOOKIE = $CONF{'USECOOKIE'};
my $LOTATION_SIZE = $CONF{'LOTATION_SIZE'};
my $EXPIREDAYS = $CONF{'EXPIREDAYS'};
my $TIMEDIFF = $CONF{'TIMEDIFF'};
my $LOTATION_SAVE = $CONF{'LOTATION_SAVE'};
my $LOCK_FLAG = $CONF{'LOCK_FLAG'};
my $IMAGE_TYPE = $CONF{'IMAGE_TYPE'};



# Remote host
my $remote_host = &GetRemoteHost;

# 指定ホストからのアクセスを除外する
if(scalar @REJECT_HOSTS) {
	my $Reject;
	my $RejectFlag = 0;
	for $Reject (@REJECT_HOSTS) {
		if($Reject =~ /[^0-9\.]/) {	# ホスト名指定の場合
			if($remote_host =~ /$Reject$/) {
				$RejectFlag = 1;
				last;
			}
		} else {	# IPアドレス指定の場合
			if($ENV{'REMOTE_ADDR'} =~ /^$Reject/) {
				$RejectFlag = 1;
				last;
			}
		}
	}
	if($RejectFlag) {
		&PrintImage;
		exit;
	}
}

#ログファイル名を決定する。
my $LOG = './logs/access_log';
my $Time = time + $TIMEDIFF*60*60;
my $DateStr = &TimeStamp($Time);
if($LOTATION == 2) {	#日ごとのローテーション
	my $DayStr = substr($DateStr, 0, 8);
	$LOG .= "\.$DayStr\.cgi";
} elsif($LOTATION == 3) {	#月ごとのローテーション
	my $MonStr = substr($DateStr, 0, 6);
	$LOG .= "\.$MonStr";
	$LOG .= '00.cgi';
} elsif($LOTATION == 4) {	#週ごとのローテーション
	my @date_array = localtime($Time);
	my $wday = $date_array[6];
	my $epoc_time = $Time;
	$epoc_time -= $wday*60*60*24;
	@date_array = localtime($epoc_time);
	my $day = $date_array[3];
	if($day < 10) {$day = "0$day";}
	my $mon = $date_array[4];
	$mon ++;	if($mon < 10) {$mon = "0$mon";}
	my $year = $date_array[5];
	$year += 1900;
	$LOG .= "\.$year$mon$day\.cgi";
} else {
	$LOG .= "\.cgi";
}


# Access Log Lotation
if($LOTATION) {
	&LogLotation;
}

# User Tracking
my %CookieList = &GetCookie;
my $TrackingData = $CookieList{'futomiacc'};
my $FirstUserFlag = 0;
unless($TrackingData) {
	$TrackingData = $ENV{'REMOTE_ADDR'}.'.'.time;
	$FirstUserFlag = 1;
}


# Remote user
my $remote_user = &GetRemoteUser;

# Requested URI
my $request = &GetRequest;

# HTTP_REFERER
my $referrer = &GetReferrer;

# Make Log String
my $LogString = &GetLogString;

# Loging
&Loging($LogString);

# Print Image to the Client
&PrintImage;
exit;



######################################################################
#  Subroutine
######################################################################

# Print Image to the Client
sub PrintImage {
	my($mime_type, $image_file);
	if($IMAGE_TYPE eq '2') {
		$mime_type = 'image/jpeg';
		$image_file = $JPEG_FILE;
	} elsif($IMAGE_TYPE eq '3') {
		$mime_type = 'image/png';
		$image_file = $PNG_FILE;
	} elsif($IMAGE_TYPE eq '1') {
		$mime_type = 'image/gif';
		$image_file = $GIF_FILE;
	} else {
		my $ua = $ENV{'HTTP_USER_AGENT'};
		if($ua =~ /J-PHONE/) {
			$mime_type = 'image/png';
			$image_file = $PNG_FILE;
		} elsif($ua =~ /UP\.Browser/) {
			$mime_type = 'image/jpeg';
			$image_file = $JPEG_FILE;
		} else {
			$mime_type = 'image/gif';
			$image_file = $GIF_FILE;
		}
	}
	open(IMAGE, "<$image_file");
	my $logo_size = -s "$image_file";
	$logo_size = -s "$image_file";
	my $data;
	read IMAGE, $data, $logo_size;
	close IMAGE;
	print "Pragma: no-cache\n";
	print "P3P: CP=\"NOI ADMa\"\n";
	if($USECOOKIE) {
		my $SetCookieString = &SetCookie('futomiacc', $TrackingData, $EXPIREDAYS);
		print "$SetCookieString\n";
	}
	print "Content-Type: $mime_type\n\n";
	print $data;
}

sub SetCookie {
	my($CookieName, $CookieValue, $ExpireDays, $Domain, $Path) = @_;
	# URLエンコード
	$CookieValue =~ s/([^\w\=\& ])/'%' . unpack("H2", $1)/eg;
	$CookieValue =~ tr/ /+/;
	my $CookieHeaderString = "Set-Cookie: $CookieName=$CookieValue\;";
	if($ExpireDays) {
		my @MonthString = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
					'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
		my @WeekString = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
		my $time = time + $ExpireDays*24*60*60;
		my($sec, $min, $hour, $monthday, $month, $year, $weekday) = gmtime($time);
		$year += 1900;
		$month = $MonthString[$month];
		if($monthday < 10) {$monthday = '0'.$monthday;}
		if($sec < 10) {$sec = '0'.$sec;}
		if($min < 10) {$min = '0'.$min;}
		if($hour < 10) {$hour = '0'.$hour;}
		my $GmtString = "$WeekString[$weekday], $monthday-$month-$year $hour:$min:$sec GMT";
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

sub Loging {
	my($String) = @_;
	open(LOGFILE, ">>$LOG") || &ErrorPrint("ログファイルをオープンできませんでした。ディレクトリ「logs」のパーミッションを確認して下さい。パーミッションを変更したら、ディレクトリ「logs」内にあるファイルをすべて削除してから、再度ブラウザーで acclog.cgi にアクセスしてみて下さい。: $!");
	if($LOCK_FLAG) {
		my $lock_result = &Lock(*LOGFILE);
		if($lock_result) {
			&ErrorPrint("ログファイルのロック処理に失敗しました。: $lock_result");
		}
	}
	print LOGFILE "$String\n";
	close(LOGFILE);
}

sub GetLogString {
	my $logfile = "$DateStr $remote_host $TrackingData $remote_user $request $referrer \"$ENV{'HTTP_USER_AGENT'}\"";
	if($ENV{'HTTP_ACCEPT_LANGUAGE'} eq '') {
		$logfile .= " \"-\"";
	} else {
		$logfile .= " \"$ENV{'HTTP_ACCEPT_LANGUAGE'}\"";
	}
	my $ScreenWidth = $q->param('width');
	my $ScreenHeight = $q->param('height');
	my $ColorDepth = $q->param('color');
	if($ScreenWidth && $ScreenHeight && $ColorDepth) {
		$logfile .= " \"$ScreenWidth $ScreenHeight $ColorDepth\"";
	} elsif($ENV{'HTTP_USER_AGENT'} =~ /J-PHONE/) {
		if($ENV{'HTTP_X_JPHONE_DISPLAY'} eq '' || $ENV{'HTTP_X_JPHONE_COLOR'} eq '') {
			$logfile .= ' "-"';
		} else {
			my($width, $height) = split(/\*/, $ENV{'HTTP_X_JPHONE_DISPLAY'});
			my $color = $ENV{'HTTP_X_JPHONE_COLOR'};
			$color =~ s/^[^0-9]+//;
			my $depth = log($color) / log(2);
			$logfile .= " \"$width $height $depth\"";
		}
	} elsif($ENV{'HTTP_USER_AGENT'} =~ /UP\.Browser/) {
		if($ENV{'HTTP_X_UP_DEVCAP_SCREENDEPTH'} eq '' || $ENV{'HTTP_X_UP_DEVCAP_SCREENPIXELS'} eq '') {
			$logfile .= ' "-"';
		} else {
			my($width, $height) = split(/,/, $ENV{'HTTP_X_UP_DEVCAP_SCREENPIXELS'});
			my($depth) = split(/,/, $ENV{'HTTP_X_UP_DEVCAP_SCREENDEPTH'});
			$logfile .= " \"$width $height $depth\"";
		}
	} else {
		$logfile .= ' "-"';
	}
	return $logfile;
}


sub GetReferrer {
	my @query_parts = split(/&/, $ENV{'QUERY_STRING'});
	my $referrer;
	my $part;
	my $flag = 0;
	for $part (@query_parts) {
		if($part =~ /^(width|height|color)=/i) {
			$flag = 0;
		}
		if($part =~ /^referrer=/i) {
			$flag = 1;
		}
		if($flag) {
			$part =~ s/^referrer=//;
			$referrer .= "$part&";
		}
	}
	$referrer =~ s/&$//;
	if($referrer eq '') {
		$referrer = '-';
	}
	$referrer =~ s/\%7e/\~/ig;
	return $referrer;
}

sub URL_encode {
	my($str) = @_;
	$str =~ s/([^\w\=\&\# ])/'%' . unpack("H2", $1)/eg;
	$str =~ tr/ /+/;
	$str =~ s/(\&)(\#)/'%' . unpack("H2", $1) . '%' . unpack("H2", $2)/eg;
	$str =~ s/(\#)/'%' . unpack("H2", $1)/eg;
	return $str;
}


sub TimeStamp {
	my($time) = @_;
	my($sec, $min, $hour, $mday, $mon, $year) = localtime($time);
	$year += 1900;
	$mon += 1;
	$mon = "0$mon" if($mon < 10);
	$mday = "0$mday" if($mday < 10);
	$hour = "0$hour" if($hour < 10);
	$min = "0$min" if($min < 10);
	$sec = "0$sec" if($sec < 10);
	my $stamp = $year.$mon.$mday.$hour.$min.$sec;
	return $stamp;
}


sub Lock {
	local(*FILE) = @_;
	eval{flock(FILE, 2)};
	if($@) {
		return $!;
	} else {
		return '';
	}
}

sub GetRequest {
	my $request = $q->param('url');
	unless($request) {
		if($ENV{'HTTP_REFERER'} eq '') {
			$request = '-';
		} else {
			$request = $ENV{'HTTP_REFERER'};
		}
	}
	$request =~ s/\%7e/\~/ig;
	return $request;
}

sub GetRemoteUser {
	my $remote_user;
	if($ENV{'REMOTE_USER'} eq '') {
		$remote_user = '-';
	} else {
		$remote_user = $ENV{'REMOTE_USER'};
	}
	return $remote_user;
}

sub GetRemoteHost {
	my $remote_host;
	if($ENV{'REMOTE_HOST'} =~ /[^0-9\.]/) {
		$remote_host = $ENV{'REMOTE_HOST'};
	} else {
		my @addr = split(/\./, $ENV{'REMOTE_ADDR'});
		my $packed_addr = pack("C4", $addr[0], $addr[1], $addr[2], $addr[3]);
		my($aliases, $addrtype, $length, @addrs);
		($remote_host, $aliases, $addrtype, $length, @addrs) = gethostbyaddr($packed_addr, 2);
		unless($remote_host) {
			$remote_host = $ENV{'REMOTE_ADDR'};
		}
	}
	return $remote_host;
}

sub LogLotation {
	my $DateStr = &TimeStamp($Time);
	$DateStr = substr($DateStr, 0, 8);
	my $log_size = -s "$LOG";
	if($LOTATION == 1) {
		if($log_size > $LOTATION_SIZE) {
			if($LOTATION_SAVE) {
				my $newlogname = $LOG;
				$newlogname =~ s/\.cgi$/\.$DateStr\.cgi/;
				rename("$LOG", "$newlogname");
			} else {
				unlink("$LOG");
			}
		}
	} elsif($LOTATION == 2 || $LOTATION == 3 || $LOTATION == 4) {
		unless($LOTATION_SAVE) {
			my @parts = split(/\//, $LOG);
			my $logname = pop @parts;
			my($logname_key) = split(/\./, $logname);
			my $logdir = join('/', @parts);
			if(opendir(DIR, "$logdir")) {
				my @files = readdir(DIR);
				closedir(DIR);
				my $file;
				for $file (@files) {
					if($file eq $logname) {
						next;
					}
					if($file =~ /^$logname_key/) {
						unlink("$logdir/$file");
					}
				}
			}
		}
	}
}

sub GetCookie {
	my(@CookieList) = split(/\; /, $ENV{'HTTP_COOKIE'});
	my %Cookie = ();
	my $key;
	for $key (@CookieList) {
		my($CookieName, $CookieValue) = split(/=/, $key);
		$CookieValue =~ s/\+/ /g;
		$CookieValue =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C",hex($1))/eg;
		$Cookie{$CookieName} = $CookieValue;
	}
	return %Cookie;
}

sub ErrorPrint {
	my($Message) = @_;
	print $q->header;
	print "$Message";
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

