# Copyright 2001-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.  For more information, consult your
# Movable Type license.
#
# $Id: MT.pm.pre 584 2006-07-11 00:50:14Z jallen $

package MT;
use strict;

use vars qw( $VERSION $VERSION_ID $SCHEMA_VERSION $PRODUCT_CODE $PRODUCT_NAME );
$VERSION = '3.3';
$VERSION_ID = '3.33-ja';  
$SCHEMA_VERSION = '3.3';
$PRODUCT_CODE = 'MT';
$PRODUCT_NAME = 'Movable Type Publishing Platform';

use MT::ConfigMgr;
use MT::Object;
use MT::Blog;
use MT::Entry;
use MT::Log;
use MT::Util qw( start_end_day start_end_week start_end_month start_end_period
                 archive_file_for get_entry extract_domains );
use File::Spec;
use File::Basename;
use Fcntl qw( LOCK_EX );

use MT::ErrorHandler;
@MT::ISA = qw( MT::ErrorHandler );

use vars qw( %Text_filters $DebugMode );
sub BEGIN {
    $DebugMode = 0;
}

sub version_number { $VERSION }
sub version_id { $VERSION_ID }
sub product_code { $PRODUCT_CODE }
sub product_name { $PRODUCT_NAME }
sub schema_version { $SCHEMA_VERSION }

sub version_slug {
    return MT->translate_templatized(<<"SLUG");
<MT_TRANS phrase="Powered by [_1]" params="$PRODUCT_NAME">
<MT_TRANS phrase="Version [_1]" params="$VERSION_ID">
<MT_TRANS phrase="http://www.sixapart.com/movabletype/">
SLUG
}

use vars qw($mt_inst %mt_inst);

sub instance {
    my $class = shift;
    $mt_inst ||= $mt_inst{$class} ||= $class->construct(@_);
}

sub set_instance {
    my $class = shift;
    $mt_inst = shift;
}

sub new {
    my $mt = &instance_of;
    $mt_inst ||= $mt;
    $mt;
}

sub instance_of {
    my $class = shift;
    $mt_inst{$class} ||= $class->construct(@_);
}

sub construct {
    my $class = shift;
    my $mt = bless { }, $class;
    local $mt_inst = $mt;
    $mt->init(@_) or
        die $mt->errstr;
    $mt;
}

# The above functions can all be used to make MT objects (and subobjects).
# The difference between them is characterized by these assertions:
# 
#  $mt = MT::App::Search->new();
#  assert($mt->isa('MT::App::Search'))
# 
#  $mt1 = MT->instance
#  $mt2 = MT->instance
#  assert($mt1 == $mt2);
# 
#  $mt1 = MT::App::CMS->construct()
#  $mt2 = MT::App::CMS->construct()
#  assert($mt1 != $mt2);
#
# TBD: make a test script for these.

sub unplug {
}

sub config {
    my $mt = shift;
    ref $mt or $mt = MT->instance;
    unless ($mt->{cfg}) {
        $mt->{cfg} = MT::ConfigMgr->instance;
    }
    if (@_) {
        my $setting = shift;
        @_ ? $mt->{cfg}->set($setting, @_) : $mt->{cfg}->get($setting);
    } else {
        $mt->{cfg};
    }
}

sub request {
    my $pkg = shift;
    my $inst = $pkg->instance;
    unless ($inst->{request}) {
        $inst->{request} = MT::Request->instance;
    }
    if (@_) {
        $inst->{request}->stash(@_);
    } else {
        $inst->{request};
    }
}

sub log {
    my $mt = shift;
    my $msg;
    if (!@_) {  # single parameter to log, so $mt must be message
        $msg = $mt;
        $mt = MT->instance;
    } else {    # multiple parameters to log; second one is message
        $msg = shift;
    }
    my $log = new MT::Log();
    if (ref $msg eq 'HASH') {
        $log->set_values($msg);
    } elsif ((ref $msg) && (UNIVERSAL::isa($msg, 'MT::Log'))) {
        $log = $msg;
    } else {
        $log->message($msg);
    }
    $log->level(MT::Log::INFO())
        unless defined $log->level;
    $log->class('system')
        unless defined $log->class;
    $log->save();
    print STDERR MT->translate("Message: [_1]", $log->message) . "\n"
        if $MT::DebugMode;
}
my $plugin_full_path;
use vars qw($plugin_sig $plugin_envelope @Plugins %Plugins);

sub add_task {
    my $mt = shift;
    require MT::TaskMgr;
    MT::TaskMgr->instance->add_task(@_);
}

sub run_tasks {
    my $mt = shift;
    $mt->init_tasks();
    MT::TaskMgr->instance->run_tasks(@_);
}

sub add_plugin {
    my $class = shift;
    my ($plugin) = @_;
    if (ref $plugin eq 'HASH') {
        require MT::Plugin;
        $plugin = new MT::Plugin($plugin);
    }
    unless ($plugin_envelope) {
        warn "MT->add_plugin improperly called outside of MT plugin load loop.";
        return;
    }
    $plugin->envelope($plugin_envelope);
    die "You cannot register multiple plugin objects from a single script."
        if exists $Plugins{$plugin_sig}{object};
    $Plugins{$plugin_sig}{object} = $plugin;
    $plugin->{name} ||= $plugin_sig;
    $plugin->{plugin_sig} = $plugin_sig;
    $plugin->{full_path} = $plugin_full_path;
    push @Plugins, $plugin if UNIVERSAL::isa($plugin, 'MT::Plugin');
    1;
}
 
use vars '@JunkFilters';

sub register_junk_filter {
    my $class = shift;
    my ($filter) = @_;
    if (!(ref $filter eq 'ARRAY')) {
        $filter = [ $filter ];
    }
    foreach (@$filter) {
        push @{$Plugins{$plugin_sig}{junk_filters}}, $_->{name} if $plugin_sig;
        $_->{plugin} ||= $Plugins{$plugin_sig} if $plugin_sig;
        push @JunkFilters, $_;
    }
}

sub add_plugin_action {
    my $class = shift;
    return MT->instance->add_plugin_action(@_) unless ref $class;
}

sub add_itemset_action {
    my $class = shift;
    return MT->instance->add_itemset_action(@_) unless ref $class;
}

sub add_log_class {
    my $mt = shift;
    MT::Log->add_class(@_);
}

use vars qw(%CallbackAlias $CallbacksEnabled);
%CallbackAlias = (
    'PreEntrySave' => 'MT::Entry::pre_save',
    'PreCommentSave' => 'MT::Comment::pre_save',
);

$CallbacksEnabled = 1;
my %CallbacksEnabled;
my @Callbacks;
sub add_callback {
    my $class = shift;
    my($meth, $priority, $plugin, $code) = @_;
    $meth = $CallbackAlias{$meth} if exists $CallbackAlias{$meth};
    my $internal = 0;
    if (ref $plugin) {
        if ((defined $mt_inst) && ($plugin == $mt_inst)) {
            $plugin = undef; $internal = 1;
        } elsif (!UNIVERSAL::isa($plugin, "MT::Plugin")) {
            return $class->trans_error("If present, 3rd argument to add_callback must be an object of type MT::Plugin");
        }
    }
    if ((ref$code) ne 'CODE') {
        return $class->trans_error('4th argument to add_callback must be a CODE reference.');
    }
    # 0 and 11 are exclusive.
    if ($priority == 0 || $priority == 11) {
        if ($Callbacks[$priority]->{$meth}) {
            return $class->trans_error("Two plugins are in conflict");
        }
    }
    return $class->trans_error("Invalid priority level [_1] at add_callback", $priority)
    if (($priority < 0) || ($priority > 11));
    require MT::Callback;
    $CallbacksEnabled{$meth} = 1;
    push @{$Plugins{$plugin_sig}{callbacks}}, "$meth Callback" if $plugin_sig;
    push @{$Callbacks[$priority]->{$meth}}, new MT::Callback(
        plugin => $plugin, 
        code => $code,
        priority => $priority,
        internal => $internal,
        method => $meth
    );
}

# For use by MT internal code
sub _register_core_callbacks {
    my $class = shift;
    my ($callback_table) = @_;
    foreach my $name (keys %$callback_table) {
        $class->add_callback($name, 5, $mt_inst, $callback_table->{$name})
            || return;
    }
    1;
}

sub register_callbacks {
    my $class = shift;
    my ($callback_list) = @_;
    foreach my $cb (@$callback_list) {
        $class->add_callback($cb->{name},
                             $cb->{priority},
                             $cb->{plugin},
                             $cb->{code})
            || return;
    }
    1;
}

use vars qw( $CB_ERR );

sub callback_error { $CB_ERR = $_[0]; }
sub callback_errstr { $CB_ERR }

sub run_callback {
    my $class = shift;
    my ($cb, @args) = @_;

    $cb->error();                         # reset the error string
    my $result = eval { $cb->invoke(@args) };
    if (my $err = $@) {
        $cb->error($err);
        my $plugin = $cb->{plugin};
        my $name;
        if ($cb->{internal}) {
            $name = "Internal callback";
        } elsif (UNIVERSAL::isa($plugin, 'MT::Plugin')) {
            $name = $plugin->name() || MT->translate("Unnamed plugin");
        } else {
            $name = MT->translate("Unnamed plugin");
        }
        MT->log({
            message => MT->translate("[_1] died with: [_2]", $name, $err),
            class => 'system',
            category => 'callback',
            level => MT::Log::ERROR(),
        });
        return 0;
    }
    if ($cb->errstr()) {
        return 0;
    }
    return $result;
}

# A callback should return a true/false value. The result of
# run_callbacks is the logical AND of all the callback's return
# values. Some hookpoints will ignore the return value: e.g. object
# callbacks don't use it. By convention, those that use it have Filter
# at the end of their names (CommentPostFilter, CommentThrottleFilter,
# etc.)
# Note: this composition is not short-circuiting. All callbacks are
# executed even if one has already returned false.
# ALSO NOTE: failure (dying or setting $cb->errstr) does not force a
# "false" return.
# THINK: are there cases where a true value should override all false values?
# that is, where logical OR is the right way to compose multiple callbacks?
sub run_callbacks {
    my $class = shift;
    my($meth, @args) = @_;
    return 1 unless $CallbacksEnabled && %CallbacksEnabled;
    $meth = $CallbackAlias{$meth} if exists $CallbackAlias{$meth};
    my @methods;
    # execution:
    #   Full::Name.<variant>
    #   *::Name.<variant> OR Name.<variant>
    #   Full::Name
    #   *::Name OR Name
    push @methods, $meth if $CallbacksEnabled{$meth}; # bleh::blah variant
    if ($meth =~ /::/) { # presence of :: implies it's an obj. cb
        my $name = $meth;
        $name =~ s/^.*::([^:]*)$/$1/;
        $name = $CallbackAlias{'*::'.$name} if exists $CallbackAlias{'*::'.$name};
        push @methods, '*::'.$name if $CallbacksEnabled{'*::'.$name}; # *::blah variant
        push @methods, $name if $CallbacksEnabled{$name}; # blah variant
    }
    if ($meth =~ /\./) { # presence of ' ' implies it is a variant callback
        my ($name) = split /\./, $meth, 2;
        $name = $CallbackAlias{$name} if exists $CallbackAlias{$name};
        push @methods, $name if $CallbacksEnabled{$name}; # bleh::blah
        if ($name =~ m/::/) {
            my $name2 = $name;
            $name2 =~ s/^.*::([^:]*)$/$1/;
            $name2 = $CallbackAlias{'*::'.$name2} if exists $CallbackAlias{'*::'.$name2};
            push @methods, '*::'.$name2 if $CallbacksEnabled{'*::'.$name2}; # *::blah
            push @methods, $name2 if $CallbacksEnabled{$name2}; # blah
        }
    }
    return 1 unless @methods;

    $CallbacksEnabled{$_} = 0 for @methods;
    my @errors;
    my $filter_value = 1;
    my $first_error;

    foreach my $callback_sheaf (@Callbacks) {
        for (@methods) {
            if (my $set = $callback_sheaf->{$_}) {
                for my $cb (@$set) {
                    my $result = $class->run_callback($cb, @args);
                    $filter_value &&= $result;
                    if (!$result) {
                        if ($cb->errstr()) {
                            push @errors, $cb->errstr();
                        }
                        if (!defined($first_error)) {
                            $first_error = $cb->errstr();
                        }
                    }
                    next unless $result;
                }
            }
        }
    }

    callback_error(join('', @errors));

    $CallbacksEnabled{$_} = 1 for @methods;
    if (!$filter_value) {
        return $class->error($first_error);
    } else {
        return $filter_value;
    }
}

sub user_class {
    shift->{user_class};
}

sub find_config {
    my $mt = shift;
    my ($param) = @_;

    $param->{Config} ||= $ENV{MT_CONFIG};
    $param->{Directory} ||= $ENV{MT_HOME};
    if (!$param->{Directory}) {
        if ($param->{Config}) {
            $param->{Directory} = dirname($param->{Config});
        } else {
            $param->{Directory} = dirname($0) || $ENV{PWD} || '.';
        }
    }

    # the directory is the more important parameter between it and
    # the config parameter. if config is unreadable, then scan for
    # a config file using the directory as a base.  we support
    # either mt.cfg or mt-config.cgi for the config file name. the
    # latter being a more secure choice since it is unreadable from
    # a browser.
    for my $cfg_file ($param->{Config},
                      File::Spec->catfile($param->{Directory}, 'mt-config.cgi'),
                      File::Spec->catfile($param->{Directory}, 'mt.cfg'),
                      'mt-config.cgi', 'mt.cfg') {
        return $cfg_file if $cfg_file && -r $cfg_file && -f $cfg_file;
    }
    return undef;
}

sub read_config {
    my $mt = shift;
    my ($param) = @_;

    my $cfg_file = $mt->find_config($param);
    return $mt->trans_error("Missing configuration file. Maybe you forgot to move mt-config.cgi-original to mt-config.cgi?") unless $cfg_file;
    if ($] >= 5.006) {
        $cfg_file = File::Spec->rel2abs($cfg_file);
    }

    # translate the config file's location to an absolute path, so we
    # can use that directory as a basis for calculating other relative
    # paths found in the config file.
    my $config_dir = $mt->{config_dir} = dirname($cfg_file);

    # store the mt_dir (home) as an absolute path; fallback to the config
    # directory if it isn't set.
    $mt->{mt_dir} = $param->{Directory}
                    ? ($] >= 5.006 ? File::Spec->rel2abs($param->{Directory}) : $param->{Directory})
                    : $mt->{config_dir};
    $mt->{mt_dir} ||= dirname($0);

    # also make note of the active application path; this is derived by
    # checking the PWD environment variable, the dirname of $0,
    # the directory of SCRIPT_FILENAME and lastly, falls back to mt_dir
    $mt->{app_dir} = $ENV{PWD} || "";
    $mt->{app_dir} = dirname($0)
        if !$mt->{app_dir} || !File::Spec->file_name_is_absolute($mt->{app_dir});
    $mt->{app_dir} = dirname($ENV{SCRIPT_FILENAME})
        if $ENV{SCRIPT_FILENAME} && (!$mt->{app_dir} || (!File::Spec->file_name_is_absolute($mt->{app_dir})));
    $mt->{app_dir} ||= $mt->{mt_dir};
    if ($] >= 5.006) {
        $mt->{app_dir} = File::Spec->rel2abs($mt->{app_dir});
    }

    my $cfg = MT::ConfigMgr->instance;
    $cfg->read_config($cfg_file) or return $mt->error($cfg->errstr);
    $mt->{cfg_file} = $cfg_file;

    my $orig_ds = $cfg->DataSource;
    my @mt_paths = $cfg->paths;
    for my $meth (@mt_paths) {
        my $path = $cfg->get($meth, undef);
        my $type = $cfg->type($meth);
        if (defined $path) {
            if ($type eq 'ARRAY') {
                my @paths = $cfg->get($meth);
                foreach (@paths) {
                    next if File::Spec->file_name_is_absolute($_);
                    $_ = File::Spec->catfile($config_dir, $_);
                }
                $cfg->$meth(\@paths);
            } else {
                if (!File::Spec->file_name_is_absolute($path)) {
                    $path = File::Spec->catfile($config_dir, $path);
                    $cfg->$meth($path);
                }
            }
        } else {
            next if $type eq 'ARRAY';
            my $path = $cfg->default($meth);
            if (defined $path) {
                $cfg->$meth(File::Spec->catfile($config_dir, $path));
            }
        }
    }

    unless (MT::Object->driver) {
        if ($orig_ds && !$cfg->ObjectDriver) {
            $cfg->ObjectDriver('DBM');
        } elsif ($cfg->ObjectDriver && ($cfg->ObjectDriver =~ /DBI::(?:mysql|postgres)/) && !$cfg->DBPassword) {
            my $pass_file = File::Spec->catfile($config_dir, 'mt-db-pass.cgi');
            if (-f $pass_file) {
                local *FH;
                if (open FH, $pass_file) {
                    my $pass = <FH>;
                    close FH;
                    if ($pass) {
                        chomp($pass);
                        $pass =~ s!^\s*!!;
                        $pass =~ s!\s*$!!;
                    }
                    $cfg->DBPassword($pass);
                }
            }
        }
        return $mt->trans_error("Bad ObjectDriver config")
            unless $cfg->ObjectDriver;

        MT::Object->set_driver($cfg->ObjectDriver)
            or return $mt->trans_error("Bad ObjectDriver config: [_1] ",
            MT::ObjectDriver->errstr);
        MT::Object->set_callback_routine(\&run_callbacks);
    }

    $cfg->read_config_db();
    MT::Object->driver->configure;

    require Data::Dumper if $cfg->DebugMode;
    $MT::DebugMode = $cfg->DebugMode || 0;

    $mt->set_language($cfg->DefaultLanguage);

    my $cgi_path = $cfg->CGIPath;
    if (!$cgi_path || $cgi_path =~ m!http://www\.example\.com/!) {
        return $mt->trans_error("Bad CGIPath config");
    }

    $mt->{cfg} = $cfg;

    1;
}

sub init {
    my $mt = shift;
    my %param = @_;

    MT->add_text_filter(__default__ => {
        label => 'Convert Line Breaks',
        on_format => sub { MT::Util::html_text_transform($_[0]) },
    });

    ## Initialize the language to the default in case any errors occur in
    ## the rest of the initialization process.
    $mt->set_language('ja');
    $mt->read_config(\%param) or return;
    $mt->init_plugins(@_) or return;
    $mt;
}

sub init_tasks {
    # Periodic Task registration
    MT->add_task({
        key => 'FuturePost',
        name => 'Publish Future Posts',
        frequency => 15 * 60,   # no more than every 15 minutes
        code => sub {
            MT->instance->publisher->publish_future_posts;
        } 
    });
    MT->add_task({
        key => 'JunkExpiration',
        name => 'Junk Folder Expiration',
        frequency => 12 * 60 * 60,  # no more than every 12 hours
        code => sub {
            require MT::JunkFilter;
            MT::JunkFilter->task_expire_junk;
        }
    });
    $_->init_tasks() foreach @MT::Plugins;
}

sub init_plugins {
    my $mt = shift;

    my $use_plugins = $mt->{cfg}->UsePlugins;
    my @PluginPaths = $mt->{cfg}->PluginPath;
    my $PluginSwitch = $mt->{cfg}->PluginSwitch || {};
    foreach my $PluginPath (@PluginPaths) {
        my $plugin_lastdir = $PluginPath;
        $plugin_lastdir =~ s![\\/]$!!;
        $plugin_lastdir =~ s!.*[\\/]!!;
        local *DH;
        if (opendir DH, $PluginPath) {
            my @p = readdir DH;
            PLUGIN:
            for my $plugin (@p) {
                next if ($plugin =~ /^\.\.?$/ || $plugin =~ /~$/);

                my $load_plugin = sub {
                    my ($plugin, $sig) = @_;
                    die "Bad plugin filename '$plugin'"
                        if ($plugin !~ /^([-\\\/\@\:\w\.\s~]+)$/);
                    local $plugin_sig = $sig;
                    $plugin = $1;
                    if (!$use_plugins || (exists $PluginSwitch->{$plugin_sig} && !$PluginSwitch->{$plugin_sig})) {
                        $Plugins{$plugin_sig}{full_path} = $plugin_full_path;
                        $Plugins{$plugin_sig}{enabled} = 0;
                        return 0;
                    }
                    return 0 if exists $Plugins{$plugin_sig};
                    $Plugins{$plugin_sig}{full_path} = $plugin_full_path;
                    eval { require $plugin };
                    if ($@) {
                        $Plugins{$plugin_sig}{error} = $@;
                        $mt->log({
                            message => $mt->translate("Plugin error: [_1] [_2]", $plugin, $Plugins{$plugin_sig}{error}),
                            class => 'system',
                            level => MT::Log::ERROR()
                        });
                        return 0;
                    }
                    $Plugins{$plugin_sig}{enabled} = 1;
                    return 1;
                };
                $plugin_full_path = File::Spec->catfile($PluginPath, $plugin);
                if (-f $plugin_full_path) {
                    $plugin_envelope = $plugin_lastdir;
                    $load_plugin->($plugin_full_path, $plugin)
                        if $plugin_full_path =~ /\.pl$/;
                } else {
                    my $plugin_dir = $plugin;
                    $plugin_envelope = "$plugin_lastdir/" . $plugin;
                    opendir SUBDIR, $plugin_full_path;
                    my @plugins = readdir SUBDIR;
                    closedir SUBDIR;
                    my $libdir;
                    (unshift @INC, $libdir)
                        if -d ($libdir = File::Spec->catdir($plugin_full_path, 'lib'));
                    for my $plugin (@plugins) {
                        next if $plugin !~ /\.pl$/;
                        my $plugin_file = File::Spec->catfile($plugin_full_path,
                                                              $plugin);
                        if (-f $plugin_file) {
                            $load_plugin->($plugin_file, $plugin_dir . '/' . $plugin);
                        }
                    }
                }
            }
            closedir DH;
        }
    }
    1;
}

*mt_dir = \&server_path;
sub server_path { $_[0]->{mt_dir} }
sub app_dir { $_[0]->{app_dir} }
sub config_dir { $_[0]->{config_dir} }

sub publisher {
    my $mt = shift;
    unless ($mt->{WeblogPublisher}) {
        require MT::WeblogPublisher;
        $mt->{WeblogPublisher} =
            new MT::WeblogPublisher();
    }
    $mt->{WeblogPublisher};
}

sub rebuild {
    my $mt = shift;
    $mt->publisher->rebuild(@_)
        or return $mt->error($mt->publisher->errstr);
}

sub rebuild_entry {
    my $mt = shift;
    $mt->publisher->rebuild_entry(@_)
        or return $mt->error($mt->publisher->errstr);
}

sub rebuild_indexes {
    my $mt = shift;
    $mt->publisher->rebuild_indexes(@_)
        or return $mt->error($mt->publisher->errstr);
}

sub ping {
    my $mt = shift;
    my %param = @_;
    my $blog;
    require MT::Entry;
    unless ($blog = $param{Blog}) {
        my $blog_id = $param{BlogID};
        $blog = MT::Blog->load($blog_id) or
            return $mt->trans_error(
                "Load of blog '[_1]' failed: [_2]", $blog_id, MT::Blog->errstr);
    }

    my(@res);

    my $send_updates = 1;
    if (exists $param{OldStatus}) {
        ## If this is a new entry (!$old_status) OR the status was previously
        ## set to draft, and is now set to publish, send the update pings.
        my $old_status = $param{OldStatus};
        if ($old_status && $old_status eq MT::Entry::RELEASE()) {
            $send_updates = 0;
        }
    }

    if ($send_updates) {
        ## Send update pings.
        my @updates = $mt->update_ping_list($blog);
        for my $url (@updates) {
            require MT::XMLRPC;
            if (MT::XMLRPC->ping_update('weblogUpdates.ping', $blog, $url)) {
                push @res, { good => 1, url => $url, type => "update" };
            } else {
                push @res, { good => 0, url => $url, type => "update",
                             error => MT::XMLRPC->errstr };
            }
        }
        if ($blog->mt_update_key) {
            require MT::XMLRPC;
            if (MT::XMLRPC->mt_ping($blog)) {
                push @res, { good => 1, url => $mt->{cfg}->MTPingURL,
                             type => "update" };
            } else {
                push @res, { good => 0, url => $mt->{cfg}->MTPingURL,
                             type => "update", error => MT::XMLRPC->errstr };
            }
        }
    }

    my $cfg = $mt->{cfg};
    my $send_tb = $cfg->OutboundTrackbackLimit;
    return \@res if $send_tb eq 'off';

    my @tb_domains;
    if ($send_tb eq 'selected') {
        @tb_domains = $cfg->OutboundTrackbackDomains;
    } elsif ($send_tb eq 'local') {
        my $iter = MT::Blog->load_iter();
        while (my $b = $iter->()) {
            next if $b->id == $blog->id;
            push @tb_domains, extract_domains($b->site_url);
        }
    }
    my $tb_domains;
    if (@tb_domains) {
        $tb_domains = '';
        my %seen;
        foreach (@tb_domains) {
            next unless $_;
            $_ = lc($_);
            next if $seen{$_};
            $tb_domains .= '|' if $tb_domains ne '';
            $tb_domains .= quotemeta($_);
            $seen{$_} = 1;
        }
        $tb_domains = '(' . $tb_domains . ')' if $tb_domains;
    }

    ## Send TrackBack pings.
    if (my $entry = $param{Entry}) {
        my $pings = $entry->to_ping_url_list;

        my %pinged = map { $_ => 1 } @{ $entry->pinged_url_list };
        my $cats = $entry->categories;
        for my $cat (@$cats) {
            push @$pings, grep !$pinged{$_}, @{ $cat->ping_url_list };
        }

        my $ua = MT->new_ua;

        ## Build query string to be sent on each ping.
        my @qs;
        push @qs, 'title=' . MT::Util::encode_url($entry->title);
        push @qs, 'url=' . MT::Util::encode_url($entry->permalink);
        push @qs, 'excerpt=' . MT::Util::encode_url($entry->get_excerpt);
        push @qs, 'blog_name=' . MT::Util::encode_url($blog->name);
        my $qs = join '&', @qs;

        ## Character encoding--best guess.
        my $enc = $mt->{cfg}->PublishCharset;

        for my $url (@$pings) {
            $url =~ s/^\s*//;
            $url =~ s/\s*$//;
            my $url_domain;
            ($url_domain) = extract_domains($url);
            next if $tb_domains && lc($url_domain) !~ m/$tb_domains$/;

            my $req = HTTP::Request->new(POST => $url);
            $req->content_type("application/x-www-form-urlencoded; charset=$enc");
            $req->content($qs);
            my $res = $ua->request($req);
            if (substr($res->code, 0, 1) eq '2') {
                my $c = $res->content;
                my($error, $msg) = $c =~
                    m!<error>(\d+).*<message>(.+?)</message>!s;
                if ($error) {
                    push @res, { good => 0, url => $url, type => 'trackback',
                                 error => $msg };
                } else {
                    push @res, { good => 1, url => $url, type => 'trackback' };
                }
            } else {
                push @res, { good => 0, url => $url, type => 'trackback',
                             error => "HTTP error: " . $res->status_line };
            }
        }
    }
    \@res;
}

sub ping_and_save {
    my $mt = shift;
    my %param = @_;
    if (my $entry = $param{Entry}) {
        my $results = $mt->ping(@_) or return;
        my %still_ping;
        my $pinged = $entry->pinged_url_list;
        for my $res (@$results) {
            next if $res->{type} ne 'trackback';
            if (!$res->{good}) {
                $still_ping{ $res->{url} } = 1;
            }
            push @$pinged, $res->{url} .
                ($res->{good} ? '' : ' ' . $res->{error});
        }
        $entry->pinged_urls(join "\n", @$pinged);
        $entry->to_ping_urls(join "\n", keys %still_ping);
        $entry->save or return $mt->error($entry->errstr);
        return $results;
    }
    1;
}

sub needs_ping {
    my $mt = shift;
    my %param = @_;
    my $blog = $param{Blog};
    my $entry = $param{Entry};
    require MT::Entry;
    return unless $entry->status == MT::Entry::RELEASE();
    my $old_status = $param{OldStatus};
    my %list;
    ## If this is a new entry (!$old_status) OR the status was previously
    ## set to draft, and is now set to publish, send the update pings.
    if (!$old_status || $old_status ne MT::Entry::RELEASE()) {
        my @updates = $mt->update_ping_list($blog);
        @list{ @updates } = (1) x @updates;
        $list{$mt->{cfg}->MTPingURL} = 1 if $blog && $blog->mt_update_key;
    }
    if ($entry) {
        @list{ @{ $entry->to_ping_url_list } } = ();
        my %pinged = map { $_ => 1 } @{ $entry->pinged_url_list };
        my $cats = $entry->categories;
        for my $cat (@$cats) {
            @list{ grep !$pinged{$_}, @{ $cat->ping_url_list } } = ();
        }
    }
    my @list = keys %list;
    return unless @list;
    \@list;
}

sub update_ping_list {
    my $mt = shift;
    my($blog) = @_;
    my @updates;
    if ($blog->ping_weblogs) {
        push @updates, $mt->config('WeblogsPingURL');
    }
    if ($blog->ping_blogs) {
        push @updates, $mt->config('BlogsPingURL');
    }
    if ($blog->ping_technorati) {
        push @updates, $mt->config('TechnoratiPingURL');
    }
    if (my $others = $blog->ping_others) {
        push @updates, split /\r?\n/, $others;
    }
    my %updates;
    for my $url (@updates) {
        for ($url) {
            s/^\s*//; s/\s*$//;
        }
        next unless $url =~ /\S/;
        $updates{$url}++;
    }
    keys %updates;
}

{
    my $LH;
    sub set_language {
        my $pkg = shift;
        require MT::L10N;
        $LH = MT::L10N->get_handle(@_);
    }

    require MT::I18N;
    sub translate {
        my $this = shift;
        my ($format, @args) = @_;
        my $enc = MT->instance->config('PublishCharset');
        return $LH->maketext(@_) if $enc =~ m/utf-?8/i;
        $format = MT::I18N::encode_text($format, $enc, 'utf-8');
        MT::I18N::encode_text($LH->maketext($format, map {MT::I18N::encode_text($_, $enc, 'utf-8')} @args),'utf-8', $enc);
    }

    sub translate_templatized {
        my $mt = shift;
        my($text) = @_;
        $text =~ s!(<MT_TRANS(?:\s+((?:\w+)\s*=\s*(["'])(?:<[^>]+?>|[^\3]+?)*?\3))+?\s*/?>)!
            my($msg, %args) = ($1);
            while ($msg =~ /\b(\w+)\s*=\s*(["'])((?:<[^>]+?>|[^\2])*?)?\2/g) {  #"
                $args{$1} = $3;
            }
            $args{params} = '' unless defined $args{params};
            my @p = map MT::Util::decode_html($_),
                    split /\s*%%\s*/, $args{params};
            @p = ('') unless @p;
            my $translation = $mt->translate($args{phrase}, @p);
            $translation =~ s/([\\'])/\\$1/sg if $args{escape};
            $translation;
        !ge;
        $text;
    }

    sub current_language { $LH->language_tag }
    sub language_handle { $LH }
}

sub supported_languages {
    my $mt = shift;
    require MT::L10N;
    require File::Basename;
    ## Determine full path to lib/MT/L10N directory...
    my $lib = 
        File::Spec->catdir(File::Basename::dirname($INC{'MT/L10N.pm'}), 'L10N');
    ## ... From that, determine full path to extlib/MT/L10N.
    ## To do that, we look for the last instance of the string 'lib'
    ## in $lib and replace it with 'extlib'. reverse is a nice tricky
    ## way of doing that.
    (my $extlib = reverse $lib) =~ s!bil!biltxe!;
    $extlib = reverse $extlib;
    my @dirs = ( $lib, $extlib );
    my %langs;
    for my $dir (@dirs) {
        opendir DH, $dir or next;
        for my $f (readdir DH) {
            my($tag) = $f =~ /^(\w+)\.pm$/;
            next unless $tag;
            my $lh = MT::L10N->get_handle($tag);
            $langs{$lh->language_tag} = $lh->language_name;
        }
        closedir DH;
    } 
    \%langs;
}

# For your convenience
sub trans_error {
    my $app = shift;
    $app->error($app->translate(@_));
}

sub add_text_filter {
    my $mt = shift;
    my($key, $cfg) = @_;
    $cfg->{label} ||= $key;
    $cfg->{on_format} ||= $cfg->{code};
    return $mt->trans_error("No executable code") unless $cfg->{on_format};
    push @{$Plugins{$plugin_sig}{text_filters}}, $cfg->{label} eq $key ? $key : $cfg->{label} . '(' . $key .')' if $plugin_sig;
    $Text_filters{$key} = $cfg;
}

sub all_text_filters { \%Text_filters }

sub apply_text_filters {
    my $mt = shift;
    my($str, $filters, @extra) = @_;
    for my $filter (@$filters) {
        next unless $Text_filters{$filter};
        $str = $Text_filters{$filter}{on_format}->($str, @extra);
    }
    $str;
}

sub new_ua {
    my $class = shift;
    eval { require LWP::UserAgent; };
    return undef if $@;
    my $cfg = MT::ConfigMgr->instance;
    if (my $localaddr = $cfg->HTTPInterface || $cfg->PingInterface) {
        @LWP::Protocol::http::EXTRA_SOCK_OPTS = (
              LocalAddr => $localaddr,
              Reuse => 1 );
    }
    my $ua = LWP::UserAgent->new;
    $ua->max_size(100_000) if $ua->can('max_size');
    $ua->agent('MovableType/' . $MT::VERSION);
    $ua->timeout($cfg->HTTPTimeout || $cfg->PingTimeout);
    if (my $proxy = $cfg->HTTPProxy || $cfg->PingProxy) {
        $ua->proxy(http => $proxy);
        my @domains = split(/,\s*/, ($cfg->HTTPNoProxy || $cfg->PingNoProxy));
        $ua->no_proxy(@domains);
    }
    $ua;        
}

sub build_email {
    my $class = shift;
    my($file, $param) = @_;
    my $cfg = MT::ConfigMgr->instance;
    my @paths = (File::Spec->catdir($cfg->TemplatePath, 'email'));
    require HTML::Template;
    my $tmpl;
    eval {
        local $1; ## This seems to fix a utf8 bug (of course).
        $tmpl = HTML::Template->new_file(
            $file,
            path => \@paths,
            search_path_on_include => 1,
            die_on_bad_params => 0,
            global_vars => 1);
    };
    return $class->trans_error("Loading template '[_1]' failed: [_2]", $file, $@) if $@;
    $tmpl->param(mt_version => MT->version_id);
    for my $key (keys %$param) {
        $tmpl->param($key, $param->{$key});
    }
    $class->translate_templatized($tmpl->output);
}

sub get_next_sched_post_for_user {
    my ($author_id, @further_blog_ids) = @_;
    require MT::Permission;
    my @perms = MT::Permission->load({author_id => $author_id}, {});
    my @blogs = @further_blog_ids;
    for my $perm (@perms) {
        next unless ($perm->can_edit_config
             || $perm->can_post
             || $perm->can_edit_all_posts);
        push @blogs, $perm->blog_id;
    }
    my $next_sched_utc = undef;
    require MT::Entry;
    for my $blog_id (@blogs) {
        my $blog = MT::Blog->load($blog_id);
        my $earliest_entry = MT::Entry->load({
            status => MT::Entry::FUTURE(),
            blog_id => $blog_id},
            {'sort' => 'created_on'}
        );
        if ($earliest_entry) {
            my $entry_utc = MT::Util::ts2iso($blog,$earliest_entry->created_on);
            if ($entry_utc < $next_sched_utc || !defined($next_sched_utc)) {
                $next_sched_utc = $entry_utc;
            }
        }
    }
    return $next_sched_utc;
}

1;
__END__

=head1 NAME

MT - Movable Type

=head1 SYNOPSIS

    use MT;
    my $mt = MT->new;
    $mt->rebuild(BlogID => 1)
        or die $mt->errstr;

=head1 DESCRIPTION

The I<MT> class is the main high-level rebuilding/pinging interface in the
Movable Type library. It handles all rebuilding operations. It does B<not>
handle any of the application functionality--for that, look to I<MT::App> and
I<MT::App::CMS>, both of which subclass I<MT> to handle application requests.

=head1 PLUGIN APPLICATIONS

At any given time, the user of the Movable Type platform is
interacting with either the core Movable Type application, or a plugin
application (or "sub-application").

A plugin application is a plugin with a user interface that inherits
functionality from Movable Type, and appears to the user as a
component of Movable Type. A plugin application typically has its own
templates displaying its own special features; but it inherits some
templates from Movable Type, such as the navigation chrome and error
pages.

=head2 The MT Root and the Application Root

To locate assets of the core Movable Type application and any plugin
applications, the platform uses two directory paths, C<mt_dir> and
C<app_dir>. These paths are returned by the MT class methods with the
same names, and some other methods return derivatives of these paths.

Conceptually, mt_dir is the root of the Movable Type installation, and
app_dir is the root of the "currently running application", which
might be Movable Type or a plugin application. It is important to
understand the distinction between these two values and what each is
used for.

The I<mt_dir> is the absolute path to the directory where MT itself is
located. Most importantly, the MT configuration file and the CGI scripts that
bootstrap an MT request are found here. This directory is also the
default base path under which MT's core templates are found (but this
can be overridden using the I<TemplatePath> configuration setting).

Likewise, the I<app_dir> is the directory where the "current"
application's assets are rooted. The platform will search for
application templates underneath the I<app_dir>, but this search also
searches underneath the I<mt_dir>, allowing the application to make
use of core headers, footers, error pages, and possibly other
templates.

In order for this to be useful, the plugin's templates and
code should all be located underneath the same directory. The relative
path from the I<app_dir> to the application's templates is
configurable. For details on how to indicate the location of your
plugin's templates, see L<MT::App>.

=head2 Finding the Root Paths

When a plugin application initializes its own application class (a
subclass of MT::App), the I<mt_dir> should be discovered and passed
constructor. This comes either from the C<Directory> parameter or the
C<Config> parameter.

Since plugins are loaded from a descendent of the MT root directory,
the plugin bootstrap code can discover the MT configuration file (and thus
the MT root directory) by traversing the filesystem; the absolute path
to that file can be passed as the C<Config> parameter to
MT::App::new. Working code to do this can be found in the
examples/plugins/mirror/mt-mirror.cgi file.

The I<app_dir>, on the other hand, always derives from the location of
the currently-running program, so it typically does not need to be
specified.

=head1 USAGE

I<MT> has the following interface. On failure, all methods return C<undef>
and set the I<errstr> for the object or class (depending on whether the
method is an object or class method, respectively); look below at the section
L<ERROR HANDLING> for more information.

=head2 MT->new( %args )

Constructs a new I<MT> instance and returns that object. Returns C<undef>
on failure.

I<new> will also read your MT configuration file (provided that it can find it--if
you find that it can't, take a look at the I<Config> directive, below). It
will also initialize the chosen object driver; the default is the C<DBM>
object driver.

I<%args> can contain:

=over 4

=item * Config

Path to the MT configuration file.

If you do not specify a path, I<MT> will try to find your MT configuration file
in the current working directory.

=item * Directory

Path to the MT home directory.

If you do not specify a path, I<MT> will try to find the MT directory using
the discovered path of the MT configuration file.

=back

=head2 MT->instance

MT and all it's subclasses are now singleton classes, meaning you can only
have one instance per package. MT->instance() returns the active instance.
MT->new() is now an alias to instance_of.

=head2 $class->instance_of

Returns the singleton instance of the MT subclass identified by C<$class>.

=head2 MT->set_instance

Assigns the active MT instance object. This value is returned when
C<MT-E<gt>instance> is invoked.

=head2 $mt->find_config($params)

Handles the discovery of the MT configuration file. The path and filename
for the configuration file is returned as the result. The C<$params>
parameter is a reference to the hash of settings passed to the MT
constructor.

=head2 $mt->read_config($params)

Reads the MT configuration settingss from the MT configuration file
and settings from database (L<MT::Config>).

The C<$params> parameter is a reference to the hash of settings passed to
the MT constructor.

=head2 $mt->init_plugins

Loads any discoverable plugins that are available. This is called from
the C<init> method, after the C<read_config> method has loaded the
configuration settings.

=head2 MT->unplug

Removes the global reference to the MT instance.

=head2 MT::log( $message ) or $mt->log( $message )

Adds an entry to the application's log table. Also writes message to
STDERR which is typically routed to the web server's error log.

=head2 $mt->server_path, $mt->mt_dir

Both of these methods return the physical file path to the directory
that is the home of the MT installation. This would be the value of
the 'Directory' parameter given in the MT constructor, or would be
determined based on the path of the configuration file.

=head2 $mt->app_dir

Returns the physical file path to the active application directory. This
is determined by the directory of the active script.

=head2 $mt->config_dir

Returns the path to the MT configuration file.

=head2 $mt->config([$setting[, $value]])

This method is used to get and set configuration settings. When called
without any parameters, it returns the active MT::ConfigMgr instance
used by the application.

Specifying the C<$setting> parameter will return the value for that setting.
When passing the C<$value> parameter, this will update the config object,
assigning that value for the named C<$setting>.

=head2 $mt->request([$element[,$data]])

The request method provides a request-scoped storage object. It is an
access interface for the L<MT::Request> package. Calling without any
parameters will return the L<MT::Request> instance.

When called with the C<$element> parameter, the data stored for that
element is returned (or undef, if it didn't exist). When called with
the C<$data> parameter, it will store the data into the specified
element in the request object.

All values placed in the request object are lost at the end of the
request. If the running application is not a web-based application,
the request object exists for the lifetime of the process and is
released when the process ends.

See the L<MT::Request> package for more information.

=head2 $mt->ping( %args )

Sends all configured XML-RPC pings as a way of notifying other community
sites that your blog has been updated.

I<%args> can contain:

=over 4

=item * Blog

An I<MT::Blog> object corresponding to the blog for which you would like to
send the pings.

Either this or C<BlogID> is required.

=item * BlogID

The ID of the blog for which you would like to send the pings.

Either this or C<Blog> is required.

=back

=head2 $mt->ping_and_save( %args )

Handles the task of issuing any pending ping operations for a given
entry and then saving that entry back to the database.

The I<%args> hash should contain an element named C<Entry> that is a
reference to a L<MT::Entry> object.

=head2 $mt->set_language($tag)

Loads the localization plugin for the language specified by I<$tag>, which
should be a valid and supported language tag--see I<supported_languages> to
obtain a list of supported languages.

The language is set on a global level, and affects error messages and all
text in the administration system.

This method can be called as either a class method or an object method; in
other words,

    MT->set_language($tag)

will also work. However, the setting will still be global--it will not be
specified to the I<$mt> object.

The default setting--set when I<MT::new> is called--is U.S. English. If a
I<DefaultLanguage> is set in the MT configuration file, the default is then
set to that language.

=head2 MT->translate($str[, $param, ...])

Translates I<$str> into the currently-set language (set by I<set_language>),
and returns the translated string. Any parameters following I<$str> are
passed through to the C<maketext> method of the active localization module.

=head2 MT->translate_templatized($str)

Translates a string that has embedded E<lt>MT_TRANSE<gt> tags. These
tags identify the portions of the string that require localization.
Each tag is processed separately and passed through the MT->translate
method. Examples (used in your application's HTML::Template templates):

    <p><MT_TRANS phrase="Hello, world"></p>

and

    <p><MT_TRANS phrase="Hello, [_1]" params="<TMPL_VAR NAME=NAME>"></p>

=head2 $mt->trans_error( $str[, $arg1, $arg2] )

Translates I<$str> into the currently-set language (set by I<set_language>),
and assigns it as the active error for the MT instance. It returns undef,
which is the usual return value upon generating an error in the application.
So when an error occurs, the typical return result would be:

    if ($@) {
        return $app->trans_error("An error occurred: [_1]", $@);
    }

The optional I<$arg1> (and so forth) parameters are passed as parameters to
any parameterized error message.

=head2 $mt->current_language

Returns the language tag for the currently-set language.

=head2 MT->supported_languages

Returns a reference to an associative array mapping language tags to their
proper names. For example:

    use MT;
    my $langs = MT->supported_languages;
    print map { $_ . " => " . $langs->{$_} . "\n" } keys %$langs;

=head2 MT->language_handle

Returns the active MT::L10N language instance for the active language.

=head2 MT->add_plugin($plugin)

Adds the plugin described by $plugin to the list of plugins displayed
on the welcome page. The argument should be an object of the
I<MT::Plugin> class.

=head2 MT->add_plugin_action($where, $action_link, $link_text)

An alias to the active L<MT::App> instance C<add_plugin_action> method.
Please refer to the L<MT::App> module for further documentation.

=head2 MT->add_text_filter($key, \%options)

Adds a text filter with the short name I<$key> and the options in
I<\%options>.

The text filter will be added to MT's list of text filtering options in
the new/edit entry screen, and will be used for filtering all of the entry
fields, if the user has enabled filtering for those fields in the template
(for example, by default the entry body and extended text are both run
through the filter, but the excerpt is not).

I<$key> should be a lower-case identifier containing only
alphanumerics and C<_> (that is, matching C</\w+/>). Since I<$key> is
stored as the filter name on a per-entry basis, it B<should not change>.
(In other words, don't call if I<foo> in one version and I<foo_bar> in
the next, if the filter does the same thing in each version.)

The flip side of this, though, is that if your filter acts differently
from one version to the next, you B<should> change I<$key>, and you
should also change the filename of your plugin, so that the old
implementation--which may be associated with all of the entries in the user's
system--still works as usual. For example, if your C<foo> plugin changes
semantics drastically so that paragraph breaks are represented as two
C<E<lt>br /E<gt>> tags, rather than C<E<lt>pE<gt>> tags, you should change
the key of the new version to C<foo_2> (for example), and the filename to
F<foo_2.pl>.

I<%options> can contain:

=over 4

=item * label

The short-but-descriptive label for the filter. This will be displayed in
the Movable Type UI as the name of the text filter.

=item * on_format

A reference to a subroutine that will be executed to filter a string of
text. The subroutine will always receive one argument, the string of text to
filter, and should return the filtered string. In some cases--for example,
when called while building a template--the subroutine will receive a
second argument, the I<MT::Template::Context> object handling the build.

See the example below.

=item * docs

The URL (or filename) of a document containing documentation on your filter.
This will be displayed in a popup window when the user selects your filter
on the New/Edit Entry screen, then clicks the Help link (C<(?)>).

If the value is a full URL (starting with C<http://>), the popup window
will open with that URL; otherwise, it is treated as a filename, assumed to
be in the user's F<docs> folder.

=back

Here's an example of adding a text filter for Wiki formatting, using the
I<Text::WikiFormat> CPAN module:

    MT->add_text_filter(wiki => {
        label => 'Wiki',
        on_format => sub {
            require Text::WikiFormat;
            Text::WikiFormat::format($_[0]);
        },
        docs => 'http://www.foo.com/mt/wiki.html',
    });

=head2 MT->all_text_filters

Returns a reference to a hash containing the registry of text filters.

=head2 MT->apply_text_filters($str, \@filters)

Applies the set of filters I<\@filters> to the string I<$str> and returns
the result (the filtered string).

I<\@filters> should be a reference to an array of filter keynames--these
are the short names passed in as the first argument to I<add_text_filter>.
I<$str> should be a scalar string to be filtered.

If one of the filters listed in I<\@filters> is not found in the list of
registered filters (that is, filters added through I<add_text_filter>),
it will be skipped silently. Filters are executed in the order in which they
appear in I<\@filters>.

As it turns out, the I<MT::Entry::text_filters> method returns a reference
to the list of text filters to be used for that entry. So, for example, to
use this method to apply filters to the main entry text for an entry
I<$entry>, you would use

    my $out = MT->apply_text_filters($entry->text, $entry->text_filters);

=head2 MT->add_callback($meth, $priority, $plugin, $code)

Registers a new callback handler for a particular registered callback.

The first parameter is the name of the callback method. The second
parameter is a priority (a number in the range of 1-10) which will control
the order that the handler is executed in relation to other handlers. If
two handlers register with the same priority, they will be executed in
the order that they registered. The third parameter is a C<MT::Plugin> object
reference that is associated with the handler (this parameter is optional).
The fourth parameter is a code reference that is invoked to handle the
callback. For example:

    MT->add_callback('BuildFile', 1, undef, \&rebuild_file_hdlr);

The code reference should expect to receive an object of type
MT::Errorhandler as its first argument. This object is used to
communicate errors to the caller:

    sub rebuild_file_hdlr {
        my ($eh, ...) = @_;
        if (something bad happens) {
            return $eh->error("Something bad happened!");
        }
    }

Other parameters to the callback function depend on the callback point.

The treatment of the error string depends on the callback point.
Typically, either it is ignored or the user's action fails and the
error message is displayed.

=head2 MT->run_callbacks($meth[, $arg1, $arg2, ...])

Invokes a particular callback, running any associated callback handlers.

The first parameter is the name of the callback to execute. This is one
of the global callback methods (see L<Callbacks> section) or can be
a class-specific method that includes the package name associated with
the callback.

The remaining arguments are passed through to any callback handlers that
are invoked.

For "Filter"-type callbacks, this routine will return a 0 if any of the
handlers return a false result. If all handlers return a true result,
a value of 1 is returned.

Example:

    MT->run_callbacks('MyClass::frobnitzes', \@whirlygigs);

Which would execute any handlers that registered in this fashion:

    MT->add_callback('MyClass::frobnitzes', 4, $plugin, \&frobnitz_hdlr);

=head2 MT->register_junk_filter( $filter )

Registers a new L<MT::JunkFilter> with Movable Type. Junk filters are
used to identify spam for incoming feedback. Please see documentation
for L<MT::JunkFilter> for more information.

Example:

    require MT::JunkFilter;
    MT->register_junk_filter(new MT::JunkFilter({
        name => "My Junk Filter",
        code => sub { $plugin->my_junk_filter(@_) },
        plugin => $plugin,
    }));

=head2 MT->version_id

Returns the version of MT (including any beta/alpha designations).

=head2 MT->version_number

Returns the numeric version of MT (without any beta/alpha designations).
For example, if I<version_id> returned C<2.5b1>, I<version_number> would
return C<2.5>.

=head2 $mt->schema_version

Returns the version of the MT database schema.

=head2 $mt->publisher

Returns the MT::WeblogPublisher object that is used for managing the
MT publishing process. See L<MT::WeblogPublisher> for more information.

=head2 $mt->build_email($file, $param)

Loads a template from the application's 'email' template directory and
processes it as a HTML::Template. The C<$param> argument is a hash reference
of parameter data for the template. The return value is the output of the
template.

=head1 ERROR HANDLING

On an error, all of the above methods return C<undef>, and the error message
can be obtained by calling the method I<errstr> on the class or the object
(depending on whether the method called was a class method or an instance
method).

For example, called on a class name:

    my $mt = MT->new or die MT->errstr;

Or, called on an object:

    $mt->rebuild(BlogID => $blog_id)
        or die $mt->errstr;

=head1 CALLBACKS

Movable Type has a variety of hook points at which a plugin can attach
a callback. The context and calling conventions of each one are
documented here.

In each case, the first parameter is an MT::ErrorHandler object which
can be used to pass error information back to the caller.

The app-level callbacks related to rebuilding are documented
below. The specific apps document the callbacks which they invoke.

=head1 LICENSE

The license that applies is the one you agreed to when downloading
Movable Type.

=head1 AUTHOR & COPYRIGHT

Except where otherwise noted, MT is Copyright 2001-2006 Six Apart.
All rights reserved.

=cut
