#!/usr/bin/perl
#******************************************************************************
#
#   PROGRAM: gcnt.cgi
#
#******************************************************************************
# gcnt.cgi VER1.1                                Author ChaichanPaPa 2000.05.25
#
#---------------------カスタマイズー-----------------------------------
require './cgi-lib.pl';
require './gifcat.pl';
$service = "./";
$imagedir = "./images/";
#----------------------------------------------------------------------
$| = 1;
&ReadParse(*in);
$mode = $in{'mode'};
$cntgif = $in{'cntgif'};
$idname = $in{'idname'};
#----------------------------------------------------------------------
if($mode == 2){      # today
   &todaycnt;
}
else{
   if($mode == 3){   # yesterday
      &yesterdaycnt;
   }
}
$pagefile = $service . $in{'idname'};
if (-e $pagefile) {	
    open COUNTER,"+<$pagefile";
    &lockf;
    $count = <COUNTER>;	
}
else{
    open COUNTER, ">$pagefile" or die "Failed open :$!";
    &lockf;
    print COUNTER "0", "\n";
    $count = 0;	
}
#
$yspagefile = $service . "ys" . $idname;
$svpagefile = $service . "sv" . $idname;
if((-e $svpagefile) == 0){
    open  SVCOUNTER, ">$svpagefile" or die "Failed open :$!";
    close SVCOUNTER;
}
open SVCOUNTER,"+<$svpagefile";
$wkSVCOUNTER = <SVCOUNTER>;
$svmday = substr $wkSVCOUNTER, 0, 2;
$svcount = substr $wkSVCOUNTER, 2;
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
if($mday < 10) { $mday = "0$mday"; }
if($mday ne $svmday){
   open  YSCOUNTER,">$yspagefile";
   $yscount =  $count - $svcount;
   print YSCOUNTER $yscount; 
   close YSCOUNTER;
   seek  SVCOUNTER, 0, 0;
   print SVCOUNTER $mday , $count;
}
close SVCOUNTER;
#
chomp $count;

$cntstr = sprintf("%ld", $count);
for ($i = 0; $i < length($cntstr); $i++) {
     $n = substr($cntstr, $i, 1);
     push(@files, $imagedir . $cntgif . "$n.gif");
}

$outgif = $imagedir . "out.gif";

open OUT, "> $outgif" or die "XXXXXX :$!", "\n";
binmode(OUT);
print OUT &gifcat'gifcat(@files);
close(OUT);

print "Content-type: image/gif\n\n";
open(IMAGE,"< $outgif");
binmode IMAGE;
binmode STDOUT;
while (<IMAGE>){
     print;
}
close IMAGE;
++$count;
seek COUNTER, 0, 0;
print COUNTER $count;
close COUNTER;
#-------------------------------------------ACCESS LOG----------------------
#($sec,$min,$hour,$mday,$mon,$year)=(localtime)[0,1,2,3,4,5];
#$accesinflog = $in{'idname'};
#$accesinflog =~ s/\.cnt/\.txt/;
#$accessf=sprintf("%s%02d%02d%s", $service, $year, $mon+1, $accesinflog);
#$yymmddhhmm=sprintf("%02d/%02d/%02d %02d:%02d ",$year,$mon+1,$mday,$hour,$min);
#open INF, ">>$accessf" or die "Failed open :$!";
#&lockf2;
#print INF $yymmddhhmm;
#print INF $ENV{'REMOTE_HOST'}, " ";
#print INF $ENV{'HTTP_USER_AGENT'}, "\n";
#close INF;
#---------------------------------------------------------------------------
exit;
sub lockf{
    flock COUNTER, 2 or die "Failed file lock :$!\n";
}
sub lockf2{
    flock INF, 2 or die "Failed file lock :$!\n";
}
#---------------------------------------------------------------------------
sub todaycnt{
    $pagefile = $service . $idname;
    open COUNTER,"<$pagefile";
    $countY = <COUNTER>;
    close COUNTER;
    $svpagefile = $service . "sv" . $in{'idname'};
    open SVCOUNTER,"<$svpagefile";
    $wkSVCOUNTER = <SVCOUNTER>;
    close SVCOUNTER;
    $svcount = substr $wkSVCOUNTER, 2;
    $count = $countY - $svcount - 1;   # -1 ha sudeni +1 sareteirutame

    $cntstr = sprintf("%ld", $count);
    for ($i = 0; $i < length($cntstr); $i++) {
         $n = substr($cntstr, $i, 1);
         push(@files, $imagedir . $cntgif . "$n.gif");
    }

    $outgif = $imagedir . "todayout.gif";

    open OUT, "> $outgif" or die "XXXXXX :$!", "\n";
    binmode(OUT);
    print OUT &gifcat'gifcat(@files);
    close(OUT);

    print "Content-type: image/gif\n\n";
    open(IMAGE,"<$outgif");
    binmode IMAGE;
    binmode STDOUT;
    while (<IMAGE>){
         print;
    }
    close IMAGE;
    exit;
}
#---------------------------------------------------------------------------
sub yesterdaycnt{
    $yspagefile = $service . "ys" . $idname;
    open YSCOUNTER, "<$yspagefile";
    $count = <YSCOUNTER>;
    close YSCOUNTER;

    $cntstr = sprintf("%ld", $count);
    for ($i = 0; $i < length($cntstr); $i++) {
         $n = substr($cntstr, $i, 1);
         push(@files, $imagedir . $cntgif . "$n.gif");
    }

    $outgif = $imagedir . "yesterdayout.gif";

    open OUT, "> $outgif" or die "XXXXXX :$!", "\n";
    binmode(OUT);
    print OUT &gifcat'gifcat(@files);
    close(OUT);

    print "Content-type: image/gif\n\n";
    open(IMAGE,"<$outgif");
    binmode IMAGE;
    binmode STDOUT;
    while (<IMAGE>){
         print;
    }
    close IMAGE;
    exit;
}
__END__
