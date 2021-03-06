# Copyright 2001-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.  For more information, consult your
# Movable Type license.
#
# $Id$

package MT::ConfigMgr;
use strict;

use MT::ErrorHandler;
@MT::ConfigMgr::ISA = qw( MT::ErrorHandler );

use vars qw( $cfg );
sub instance {
    return $cfg if $cfg;
    $cfg = __PACKAGE__->new;
}

sub new {
    my $mgr = bless { __var => { }, __dbvar => { }, __paths => [] }, $_[0];
    $mgr->init;
    $mgr;
}

sub init {
    my $mgr = shift;
    $mgr->define([
        ['AtomApp', { Type => 'HASH',
                      Default => 'weblog=MT::AtomServer::Weblog' }],
        ['SchemaVersion'],
        ['DataSource', { Path => 1 }],
        ['Database'],
        ['DBHost'],
        ['DBSocket'],
        ['DBPort'],
        ['DBUser'],
        ['DBPassword'],
        ['DefaultLanguage', { Default => 'ja' }],
        ['DefaultSiteRoot', { Default => '' }],
        ['DefaultSiteURL', { Default => '' }],
        ['TemplatePath', { Default => 'tmpl', Path => 1 } ],
        ['WeblogTemplatesPath', { Default => 'default_templates', Path => 1 } ],
        ['AltTemplatePath', { Default => 'alt-tmpl', Path => 1 }],
        ['CSSPath', { Default => 'css' } ],
        ['ImportPath', { Default => 'import', Path => 1 } ],
        ['PluginPath', { Default => 'plugins', Path => 1, Type => 'ARRAY' } ],
        ['EnableArchivePaths', { Default => 0 }],
        ['SearchTemplatePath', { Default => 'search_templates', Path => 1 } ],
        ['ObjectDriver'],
        ['Serializer', { Default => 'MT' }],
        ['SendMailPath', { Default => '/usr/lib/sendmail' }],
        ['TimeOffset', { Default => 0 }],
        ['WSSETimeout', { Default => 120 }],
        ['StaticWebPath', { Default => '' }],
        ['CGIPath', { Default => '/cgi-bin/' }],
        ['AdminCGIPath'],
        ['CookieDomain'],
        ['CookiePath'],
        ['MailEncoding', { Default => 'ISO-2022-JP' }],
        ['MailTransfer', { Default => 'sendmail' }],
        ['SMTPServer', { Default => 'localhost' }],
        ['DebugEmailAddress'],
        ['WeblogsPingURL', { Default => 'http://rpc.weblogs.com/RPC2' }],
        ['BlogsPingURL', { Default => 'http://ping.blo.gs/' }],
        ['MTPingURL', { Default => 'http://www.movabletype.org/update/' }],
        ['TechnoratiPingURL', 
                 { Default => 'http://rpc.technorati.com/rpc/ping' }],
        ['CGIMaxUpload', { Default => 1_000_000 }],
        ['DBUmask', { Default => '0111' }],
        ['HTMLUmask', { Default => '0111' }],
        ['UploadUmask', { Default => '0111' }],
        ['DirUmask', { Default => '0000' }],
        ['HTMLPerms', { Default => '0666' }],
        ['UploadPerms', { Default => '0666' }],
        ['NoTempFiles', { Default => 0 }],
        ['TempDir', { Default => '/tmp' }],
        ['EntriesPerRebuild', { Default => 40 }],
        ['UseNFSSafeLocking', { Default => 0 }],
        ['NoLocking', { Default => 0 }],
        ['NoHTMLEntities', { Default => 1 }],
        ['NoCDATA', { Default => 0 }],
        ['NoPlacementCache', { Default => 0 }],
        ['NoPublishMeansDraft', { Default => 0 }],
        ['IgnoreISOTimezones', { Default => 0 }],
        ['PingTimeout', { Default => 60 }],
        ['HTTPTimeout', { Default => 60 }],
        ['PingInterface'],
        ['HTTPInterface'],
        ['PingProxy'],
        ['HTTPProxy'],
        ['PingNoProxy', { Default => 'localhost' }],
        ['HTTPNoProxy', { Default => 'localhost' }],
        ['ImageDriver', { Default => 'ImageMagick' }],
        ['NetPBMPath'],
        ['AdminScript', { Default => 'mt.cgi' }],
        ['ActivityFeedScript', { Default => 'mt-feed.cgi' }],
        ['ActivityFeedItemLimit', { Default => 50 }],
        ['CommentScript', { Default => 'mt-comments.cgi' }],
        ['TrackbackScript', { Default => 'mt-tb.cgi' }],
        ['SearchScript', { Default => 'mt-search.cgi' }],
        ['XMLRPCScript', { Default => 'mt-xmlrpc.cgi' }],
        ['ViewScript', { Default => 'mt-view.cgi' }],
        ['AtomScript', { Default => 'mt-atom.cgi' }],
        ['UpgradeScript', { Default => 'mt-upgrade.cgi' }],
        ['PublishCharset', { Default => 'UTF-8' }],
        ['SafeMode', { Default => 1 }],
        ['GlobalSanitizeSpec', { Default => 'a href,b,i,br/,p,strong,em,ul,ol,li,blockquote,pre' }],
        ['GenerateTrackBackRSS', { Default => 0 }],

    ## Search settings, copied from Jay's mt-search and integrated
    ## into default config.
        ['NoOverride', { Default => '' }],
        ['RegexSearch', { Default => 0 }],
        ['CaseSearch', { Default => 0 }],
        ['ResultDisplay', { Default => 'descend' }],
        ['ExcerptWords', { Default => 40 }],
        ['SearchElement', { Default => 'entries' }],
        ['ExcludeBlogs'],
        ['IncludeBlogs'],
        ['DefaultTemplate', { Default => 'default.tmpl' }],
        ['Type', { Default => 'straight' }],
        ['MaxResults', { Default => '9999999' }],
        ['SearchCutoff', { Default => '9999999' }],
        ['CommentSearchCutoff', { Default => '30' }],
        ['AltTemplate', { Type => 'ARRAY', Default => 'feed results_feed.tmpl' }],
        ['SearchSortBy'],
        ['SearchSortOrder', { Default => 'ascend' }],
        ['RegKeyURL', { Default => 
         'http://www.typekey.com/extras/regkeys.txt' }],
        ['IdentitySystem', { Default => 'http://www.typekey.com/t/typekey' }],
        ['SignOnURL', { Default => 
         'https://www.typekey.com/t/typekey/login?' }],
        ['SignOffURL', { Default => 
         'https://www.typekey.com/t/typekey/logout?' }],
        ['IdentityURL', { Default => "http://profile.typekey.com/" }],
        ['DynamicComments', { Default => 0 }],
        ['SignOnPublicKey', { Default => '' }],
        ['ThrottleSeconds', { Default => 20 }],
        ['SearchThrottleIPWhitelist'],
        ['OneHourMaxPings', { Default => 10 }],
        ['OneDayMaxPings', { Default => 50 }],
        ['SupportURL' => { Default => 'http://www.sixapart.jp/movabletype/support/' }],
        ['NewsURL', { Default => 'http://www.sixapart.jp/movabletype/' }],
        ['NewsboxURL', { Default => 'http://www.sixapart.jp/movabletype/news/newsbox.html' }],
        ['EmailAddressMain'],
        ['EmailReplyTo'],
        ['EmailVerificationSecret'],
        ['EmailNotificationBcc', { Default => 1 }],
        ['CommentSessionTimeout', { Default => 60 * 60 * 1 }],
        ['UserSessionTimeout', { Default => 60 * 60 * 4 }],
        ['LaunchBackgroundTasks', { Default => 0 }],
        ['TypeKeyVersion', { Default => '1.1' }],
        ['TransparentProxyIPs', { Default => 0 }],
        ['DebugMode', { Default => 0 }],
        ['PublishCommenterIcon', { Default => 1 }],
        ['ShowIPInformation', { Default => 0 }],
        ['AllowComments', {Default => 1}],
        ['AllowPings', {Default => 1}],
        ['HelpURL', {Default => 'http://www.sixapart.jp/movabletype/manual/' . MT->version_number . '/'}],
        ['UsePlugins', {Default => 1}],
        ['PluginSwitch', {Type => 'HASH'}],
        ['PluginSchemaVersion', {Type => 'HASH'}],
        ['OutboundTrackbackLimit', { Default => 'any' }],
        ['OutboundTrackbackDomains', { Type => 'ARRAY' } ],
        ['IndexBasename', {Default => 'index'}],
        ['LogExportEncoding', {Default => 'Shift_JIS'}],
        ['ActivityFeedsRunTasks', {Default => 1}],
        ['ExportEncoding', {Default => 'Shift_JIS'}],
        ['SQLSetNames'],
        ['UseSQLite2', { Default => 0 } ],
        ['UseJcodeModule', { Default => 0 } ],
        ['DefaultTimezone', { Default => '9' } ],
        ['CategoryNameNodash', { Default => '1' } ],
        ['DefaultListPrefs', {Type => 'HASH',
                              Default => {
                                  Rows => 20,
                                  Format => 'Compact',      # Compact|Expanded
                                  SortOrder => 'Ascend',    # Ascend|Descend
                                  Button => 'Above',        # Above|Below|Both
                                  DateFormat => 'Relative', # Relative|Full
                              }
                             }],
        ['DefaultEntryPrefs', {Type => 'HASH',
                               Default => {
                                   Type => 'Basic',   # Basic|All|Custom
                                   Button => 'Below', # Above|Below|Both
                               }
                             }],
        ['DeleteFilesAtRebuild', { Default => 0 } ],
    ]);
}

sub define {
    my $mgr = shift;
    my($vars);
    if (ref $_[0] eq 'ARRAY') {
        $vars = shift;
    } else {
        my($var, %param) = @_;
        $vars = [ [ $var, \%param ] ];
    }
    foreach my $def (@$vars) {
        my($var, $param) = @$def;
        $mgr->{__var}{$var} = undef;
        $mgr->{__settings}{$var} = keys %$param ? { %$param } : {};
        if ($mgr->{__settings}{$var}{Path}) {
            push @{$mgr->{__paths}}, $var;
        }
    }
}

sub paths {
    my $mgr = shift;
    wantarray ? @{$mgr->{__paths}} : $mgr->{__paths};
}

sub get {
    my $mgr = shift;
    my $var = shift;
    my $val;
    if (defined($val = $mgr->{__var}{$var})) {
        wantarray && ($mgr->{__settings}{$var}{Type}||'') eq 'ARRAY' ?
            @$val : ((ref $val) eq 'ARRAY' && @$val ? $val->[0] : $val);
    } elsif (defined($val = $mgr->{__dbvar}{$var})) {
        wantarray && ($mgr->{__settings}{$var}{Type}||'') eq 'ARRAY' ?
            @$val : ((ref $val) eq 'ARRAY' && @$val ? $val->[0] : $val);
    } else {
        $mgr->default($var);
    }
}

sub type {
    my $mgr = shift;
    my $var = shift;
    $mgr->{__settings}{$var}{Type} || 'SCALAR';
}

sub default {
    my $mgr = shift;
    my $var = shift;
    my $def = $mgr->{__settings}{$var}{Default};
    return undef unless defined $def;
    if (my $type = $mgr->{__settings}{$var}{Type}) {
        if ($type eq 'ARRAY') {
            return wantarray ? ( $def ) : $def;
        } elsif ($type eq 'HASH') {
            if (ref $def ne 'HASH') {
                (my($key), my($val)) = split /=/, $def;
                return { $key => $val };
            }
        }
    }
    $def;
}

sub set {
    my $mgr = shift;
    my($var, $val, $db_flag) = @_;
    $db_flag ||= exists $mgr->{__dbvar}{$var};
    my $set = $db_flag ? '__dbvar' : '__var';
    if (my $type = $mgr->{__settings}{$var}{Type}) {
        if ($type eq 'ARRAY') {
            if (ref $val eq 'ARRAY') {
                $mgr->{$set}{$var} = $val;
            } else {
                $mgr->{$set}{$var} ||= [];
                push @{ $mgr->{$set}{$var} }, $val if defined $val;
            }
        } elsif ($type eq 'HASH') {
            $mgr->{$set}{$var} = $mgr->default($var)
                if !defined $mgr->{$set}{$var};
            if (ref $val eq 'HASH') {
                $mgr->{$set}{$var} = $val;
            } else {
                $mgr->{$set}{$var} ||= {};
                (my($key), $val) = split /=/, $val;
                $mgr->{$set}{$var}{$key} = $val;
            }
        } else {
            $mgr->{$set}{$var} = $val;
        }
    } else {
        $mgr->{$set}{$var} = $val;
    }
}

sub read_config {
    my $class = shift;
    $class->read_config_file(@_);
}

sub save_config {
    my $class = shift;
    my $mgr = $class->instance;
    my $data = '';
    my $settings = $mgr->{__dbvar};
    foreach (sort keys %$settings) {
        my $type = ($mgr->{__settings}{$_}{Type}||'');
        if ($type eq 'HASH') {
            my $h = $settings->{$_};
            foreach my $k (keys %$h) {
                $data .= $_ . ' ' . $k . '=' . $h->{$k} . "\n";
            }
        } elsif ($type eq 'ARRAY') {
            my $a = $settings->{$_};
            foreach my $v (@$a) {
                $data .= $_ . ' ' . $v . "\n";
            }
        } else {
            $data .= $_ . ' ' . $settings->{$_} . "\n";
        }
    }
    require MT::Config;
    my ($config) = MT::Config->load() || new MT::Config;
    $config->data($data);
    $config->save or die $config->errstr;
}

sub read_config_file {
    my $class = shift;
    my($cfg_file) = @_;
    my $mgr = $class->instance;
    $mgr->{__var} = {};
    local(*FH, $_, $/);
    $/ = "\n";
    die "Can't read config without config file name" if !$cfg_file;
    open FH, $cfg_file or
        return $class->error(MT->translate(
            "Error opening file '[_1]': [_2]", $cfg_file, "$!" ));
    my $line;
    while (<FH>) {
        chomp; $line++;
        next if !/\S/ || /^#/;
        my($var, $val) = $_ =~ /^\s*(\S+)\s+(.*)$/;
        return $class->error(MT->translate("Config directive [_1] without value at [_2] line [_3]", $var, $cfg_file, $line))
            unless defined($val) && $val ne '';
        $val =~ s/\s*$//;
        next unless $var && defined($val);
        #return $class->error(MT->translate(
        #    "[_1]:[_2]: variable '[_3]' not defined", $cfg_file, $., $var
        #    )) unless exists $mgr->{__settings}->{$var};
        next unless exists $mgr->{__settings}->{$var};
        $mgr->set($var, $val);
    }
    close FH;
    1;
}

sub read_config_db {
    my $class = shift;
    my $mgr = $class->instance;
    require MT::Config;
    my ($config) = eval { MT::Config->load() };
    if ($config) {
        my $data = $config->data;
        my @data = split /[\r?\n]/, $data;
        my $line = 0;
        foreach (@data) {
            $line++;
            chomp;
            next if !/\S/ || /^#/;
            my($var, $val) = $_ =~ /^\s*(\S+)\s+(.+)$/;
            $val =~ s/\s*$//;
            next unless $var && defined($val);
            #return $class->error(MT->translate(
            #    "[_1]:[_2]: variable '[_3]' not defined", "database", $line, $var
            #)) unless exists $mgr->{__settings}->{$var};

            # ignore setting if it isn't defined...
            next unless exists $mgr->{__settings}->{$var};
            $mgr->set($var, $val, 1);
        }
    }
    1;
}

sub DESTROY { }

use vars qw( $AUTOLOAD );
sub AUTOLOAD {
    my $mgr = $_[0];
    (my $var = $AUTOLOAD) =~ s!.+::!!;
    return $mgr->error(MT->translate("No such config variable '[_1]'", $var))
        unless exists $mgr->{__settings}->{$var};
    no strict 'refs';
    *$AUTOLOAD = sub {
        my $mgr = shift;
        @_ ? $mgr->set($var, @_) : $mgr->get($var);
    };
    goto &$AUTOLOAD;
}

1;
__END__

=head1 NAME

MT::ConfigMgr - Movable Type configuration manager

=head1 SYNOPSIS

    use MT::ConfigMgr;
    my $cfg = MT::ConfigMgr->instance;

    $cfg->read_config('/path/to/mt.cfg')
        or die $cfg->errstr;

=head1 DESCRIPTION

I<MT::ConfigMgr> is a singleton class that manages the Movable Type
configuration file (F<mt.cfg>), allowing access to the config directives
contained therin.

=head1 USAGE

=head2 MT::ConfigMgr->instance

Returns the singleton I<MT::ConfigMgr> object. Note that when you want the
object, you should always call I<instance>, never I<new>; I<new> will construct
a B<new> I<MT::ConfigMgr> object, and that isn't what you want. You want the
object that has already been initialized with the contents of F<mt.cfg>. This
initialization is done by I<MT::new>.

=head2 $cfg->read_config($file)

Reads the config file at the path I<$file> and initializes the I<$cfg> object
with the directives in that file. Returns true on success, C<undef> otherwise;
if an error occurs you can obtain the error message with C<$cfg-E<gt>errstr>.

=head2 $cfg->define($directive [, %arg ])

Defines the directive I<$directive> as a valid configuration directive; you
must define new configuration directives B<before> you read the configuration
file, or else the read will fail.

=head1 CONFIGURATION DIRECTIVES

The following configuration directives are allowed in F<mt.cfg>. To get the
value of a directive, treat it as a method that you are calling on the
I<$cfg> object. For example:

    $cfg->CGIPath

To set the value of a directive, do the same as the above, but pass in a value
to the method:

    $cfg->CGIPath('http://www.foo.com/mt/');

A list of valid configuration directives can be found in the
I<CONFIGURATION SETTINGS> section of the manual.

=head1 AUTHOR & COPYRIGHT

Please see the I<MT> manpage for author, copyright, and license information.

=cut
