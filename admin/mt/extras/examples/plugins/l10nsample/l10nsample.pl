# Copyright 2005-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.
#
# $Id: l10nsample.pl 2 2006-06-09 23:16:03Z hachi $

package MT::Plugin::l10nsample;

use strict;
use base 'MT::Plugin';
use vars qw($VERSION);
$VERSION = '0.01';

my $plugin;
$plugin = MT::Plugin::l10nsample->new({
    name => "<MT_TRANS phrase=\"l10nsample\">",
    version => $VERSION,
    doc_link => "http://www.sixapart.com/",
    description => "<MT_TRANS phrase=\"This description can be localized if there is l10n_class set.\">",
    author_name => "<MT_TRANS phrase=\"Fumiaki Yoshimatsu\">",
    author_link => "http://sixapart.com/",
    l10n_class => 'l10nsample::L10N',
});
MT->add_plugin($plugin);
MT->add_plugin_action('blog', 'l10nsample.cgi', 'This is localizable');

sub instance { $plugin }