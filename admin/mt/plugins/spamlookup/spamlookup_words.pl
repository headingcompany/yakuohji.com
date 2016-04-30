# SpamLookup plugin for Movable Type
# Original copyright (c) 2004-2006, Brad Choate and Tobias Hoellrich
# Author: Six Apart (http://www.sixapart.com)
# Released under the Artistic License
#
# $Id: spamlookup_words.pl 48 2006-06-13 19:55:17Z jallen $

package MT::Plugin::SpamLookup::KeywordFilter;

use strict;
use MT;
use MT::Plugin;

use vars qw($VERSION);
sub BEGIN {
    @MT::Plugin::SpamLookup::KeywordFilter::ISA = ('MT::Plugin');
    $VERSION = '2.1';
    my $plugin;
    $plugin = new MT::Plugin::SpamLookup::KeywordFilter({
        name => 'SpamLookup - Keyword Filter',
        version => $VERSION,
        description => '<MT_TRANS phrase="SpamLookup module for moderating and junking feedback using keyword filters.">',
        doc_link => 'http://www.spamlookup.com/wiki/KeywordFilter',
        author_name => 'Six Apart, Ltd.',
        author_link => 'http://www.sixapart.com/',
        config_template => 'word_config.tmpl',
        l10n_class => 'spamlookup::L10N',
        settings => new MT::PluginSettings([
            ['wordlist_moderate'],
            ['wordlist_junk', { Default => q{# Your Junk keyword list can contain words, phrases, patterns,
# and domain names. Each item must be on a separate line.
#
# Words and phrases can be listed plainly. They are tested in a
# case-insensitive manner and match against "whole" words:
cialis

# Patterns are Perl regular expressions.
/online-?casino/i

# You can optionally place a score at the end of the line to adjust
# the penalty applied for matching that item.
phentermine 4}} ],
        ])
    });
    MT->add_plugin($plugin);
    MT->register_junk_filter({
        code => sub { $plugin->runner('wordfilter', @_) },
        plugin => $plugin,
        name => 'SpamLookup Keyword Filter'
    });
}

sub runner {
    my $plugin = shift;
    my $method = shift;
    require spamlookup;
    return $_->($plugin, @_) if $_ = \&{"spamlookup::$method"};
    die "Failed to find spamlookup::$method";
}

sub apply_default_settings {
    my $plugin = shift;
    my ($data, $scope) = @_;
    if ($scope ne 'system') {
        my $sys = $plugin->get_config_obj('system');
        my $sysdata = $sys->data();
        if ($plugin->{settings} && $sysdata) {
            foreach (keys %$sysdata) {
                $data->{$_} = $sysdata->{$_} if !exists $data->{$_};
            }
        }
    } else {
        $plugin->SUPER::apply_default_settings(@_);
    }
}

1;
