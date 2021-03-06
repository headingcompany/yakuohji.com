# Copyright 2001-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.  For more information, consult your
# Movable Type license.
#
# $Id: Entry.pm 575 2006-07-08 18:00:12Z jallen $

package MT::Entry;
use strict;

use MT::Blog;
use MT::Author;
use MT::Category;
use MT::Placement;
use MT::Comment;
use MT::Util qw( archive_file_for discover_tb start_end_period extract_domain
                 extract_domains );
use MT::Tag;

use MT::Object;
@MT::Entry::ISA = qw( MT::Object MT::Taggable );
__PACKAGE__->install_properties({
    column_defs => {
        'id' => 'integer not null auto_increment',
        'blog_id' => 'integer not null',
        'status' => 'smallint not null',
        'author_id' => 'integer not null',
        'allow_comments' => 'boolean',
        'title' => 'string(255)',
        'excerpt' => 'text',
        'text' => 'text',
        'text_more' => 'text',
        'convert_breaks' => 'string(30)',
        'to_ping_urls' => 'text',
        'pinged_urls' => 'text',
        'allow_pings' => 'boolean',
        'keywords' => 'text',
        'tangent_cache' => 'text',
        'basename' => 'string(255)',
        'atom_id' => 'string(255)',
        'week_number' => 'integer',
## Have to keep this around for use in mt-upgrade.cgi.
        'category_id' => 'integer',
    },
    indexes => {
        blog_id => 1,
        status => 1,
        author_id => 1,
        created_on => 1,
        modified_on => 1,
        week_number => 1,
        basename => 1,
    },
    child_of => 'MT::Blog',
    audit => 1,
    datasource => 'entry',
    primary_key => 'id',
});

use constant HOLD    => 1;
use constant RELEASE => 2;
use constant REVIEW  => 3;
use constant FUTURE  => 4;

use Exporter;
*import = \&Exporter::import;
use vars qw( @EXPORT_OK %EXPORT_TAGS);
@EXPORT_OK = qw( HOLD RELEASE FUTURE );
%EXPORT_TAGS = (constants => [ qw(HOLD RELEASE FUTURE) ]);

sub status_text {
    my $s = $_[0];
    $s == HOLD ? "Draft" :
        $s == RELEASE ? "Publish" :
            $s == REVIEW ? "Review" : 
            $s == FUTURE ? "Future" : '';
}

sub status_int {
    my $s = lc $_[0];   ## Lower-case it so that it's case-insensitive
    $s eq 'draft' ? HOLD :
        $s eq 'publish' ? RELEASE :
            $s eq 'review' ? REVIEW :
                $s eq 'future' ? FUTURE : undef;
}

sub next {
    my $entry = shift;
    my($publish_only) = @_;
    $publish_only = $publish_only ? {status => RELEASE} : {};
    $entry->_nextprev('next', $publish_only);
}

sub previous {
    my $entry = shift;
    my($publish_only) = @_;
    $publish_only = $publish_only ? {status => RELEASE} : {};
    $entry->_nextprev('previous', $publish_only);
}

sub _nextprev {
    my $obj = shift;
    my $class = ref($obj);
    my ($direction, $publish_only) = @_;
    return undef unless ($direction eq 'next' || $direction eq 'previous');
    my $next = $direction eq 'next';

    my $label = '__' . $direction;
    return $obj->{$label} if $obj->{$label};

    # Selecting the adjacent object can be tricky since timestamps
    # are not necessarily unique for entries. If we find that the
    # next/previous object has a matching timestamp, keep selecting entries
    # to select all entries with the same timestamp, then compare them using
    # id as a secondary sort column.

    my ($id, $ts) = ($obj->id, $obj->created_on);
    my $iter = $class->load_iter({
        blog_id => $obj->blog_id,
        created_on => ($next ? [ $ts, undef ] : [ undef, $ts ]),
        %{$publish_only}
    }, {
        'sort' => 'created_on',
        'direction' => $next ? 'ascend' : 'descend',
        'range_incl' => { 'created_on' => 1 },
    });

    # This selection should always succeed, but handle situation if
    # it fails by returning undef.
    return unless $iter;

    # The 'same' array will hold any entries that have matching
    # timestamps; we will then sort those by id to find the correct
    # adjacent object.
    my @same;
    while (my $e = $iter->()) {
        # Don't consider the object that is 'current'
        next if $e->id == $id;
        my $e_ts = $e->created_on;
        if ($e_ts eq $ts) {
            # An object with the same timestamp should only be
            # considered if the id is in the scope we're looking for
            # (greater than for the 'next' object; less than for
            # the 'previous' object).
            push @same, $e
                if $next && $e->id > $id or !$next && $e->id < $id;
        } else {
            # We found an object with a timestamp different than
            # the 'current' object.
            if (!@same) {
                push @same, $e;
                # We should check to see if this new timestamped object also
                # has entries adjacent to _it_ that have the same timestamp.
                while (my $e = $iter->()) {
                    push(@same, $e), next if $e->created_on eq $e_ts;
                    $iter->('finish'), last;
                }
            } else {
                $iter->('finish');
            }
            return $obj->{$label} = $e unless @same;
            last;
        }
    }
    if (@same) {
        # If we only have 1 element in @same, return that.
        return $obj->{$label} = $same[0] if @same == 1;
        # Sort remaining elements in @same by id.
        @same = sort { $a->id <=> $b->id } @same;
        # Return front of list (smallest id) if selecting 'next'
        # object. Return tail of list (largest id) if selection 'previous'.
        return $obj->{$label} = $same[$next ? 0 : $#same];
    }
    return;
}

sub trackback {
    my $entry = shift;
    if (@_) {
        $entry->{__trackback} = shift;
    } elsif (!$entry->{__trackback} && $entry->id) {
        my $tb = MT::Trackback->load({ entry_id => $entry->id });
        $entry->{__trackback} = $tb;
    }
    $entry->{__trackback};
}

sub author {
    my $entry = shift;
    my $req = MT::Request->instance();
    unless ($entry->{__author}) {
        my $author_cache = $req->stash('author_cache');
        $entry->{__author} = $author_cache->{$entry->author_id};
        unless ($entry->{__author}) {
            require MT::Author;
            $entry->{__author} = MT::Author->load($entry->author_id,
                                                  {cached_ok=>1});
            $author_cache->{$entry->author_id} = $entry->{__author};
            $req->stash('author_cache', $author_cache);
        }
    }
    $entry->{__author};
}

## To speed up <$MTEntryCategory$> (and category-loading in general),
## the first time either ->category or ->categories is used, we load the
## list of placements (entry-category mappings) into memory into an
## MT::Request object. Lookups to determine if an entry has a category are
## thus very fast. We add a new config setting NoPlacementCache in case
## this causes problems for anyone. :)

sub _placement_cache {
    my($blog_id) = @_;
    my $r = MT::Request->instance;
    my $cache = $r->cache('all_placements');
    unless ($cache->{$blog_id}) {
        $cache->{$blog_id} = {};
        $r->cache('all_placements', $cache);
        require MT::Placement;
        my @p = MT::Placement->load({ blog_id => $blog_id });
        for my $p (@p) {
            push @{ $cache->{$blog_id}{all}{$p->entry_id} }, $p->category_id;
            $cache->{$blog_id}{primary}{$p->entry_id} = $p->category_id
                if $p->is_primary;
        }
    }
    $cache->{$blog_id};
}

sub reset_placement_cache {
    my $entry = shift;
    if (ref $entry) {
        delete $entry->{__category};
        delete $entry->{__categories};
    }
    require MT::Category;
    return if MT::ConfigMgr->instance->NoPlacementCache;
    my $r = MT::Request->instance;
    my $cache = $r->cache('all_placements');
    return unless $cache;
    if (ref $entry) {
        my $blog_id = $entry->blog_id;
        my $entry_id = $entry->id;
        if ($cache->{$blog_id}) {
            delete $cache->{$blog_id}{all}{$entry_id};
            delete $cache->{$blog_id}{primary}{$entry_id};
        }
    } else {
        $r->cache('all_placements', {});
    }
}

sub category {
    my $entry = shift;
    unless ($entry->{__category}) {
        require MT::Category;
        unless (MT::ConfigMgr->instance->NoPlacementCache) {
            my $cache = _placement_cache($entry->blog_id);
            if (exists $cache->{primary}{$entry->id}) {
                my $p = $cache->{primary}{$entry->id} or return;
                return $entry->{__category} = MT::Category->load($p,
                    {cached_ok=>1});
            }
        }
        require MT::Placement;
        $entry->{__category} = MT::Category->load(undef,
            { 'join' => [ 'MT::Placement', 'category_id',
                        { entry_id => $entry->id,
                          is_primary => 1 } ] },
        );
    }
    $entry->{__category};
}

sub categories {
    my $entry = shift;
    unless ($entry->{__categories}) {
        require MT::Category;
        unless (MT::ConfigMgr->instance->NoPlacementCache) {
            my $cache = _placement_cache($entry->blog_id);
            if (exists $cache->{all}{$entry->id}) {
                my $p = $cache->{all}{$entry->id} or return;
                for my $place (@$p) {
                    push @{ $entry->{__categories} },
                        MT::Category->load($place, {cached_ok=>1});
                }
                $entry->{__categories} = [ sort { $a->label cmp $b->label }
                                           @{ $entry->{__categories} } ];
                return $entry->{__categories};
            }
        }
        require MT::Placement;
        $entry->{__categories} = [ MT::Category->load(undef,
            { 'join' => [ 'MT::Placement', 'category_id',
                        { entry_id => $entry->id } ] },
        ) ];
        $entry->{__categories} = [ sort { $a->label cmp $b->label }
                                   @{ $entry->{__categories} } ];
    }
    $entry->{__categories};
}

sub is_in_category {
    my $entry = shift;
    my($cat) = @_;
    my $cats = $entry->categories;
    for my $c (@$cats) {
        return 1 if $c->id == $cat->id;
    }
    0;
}

sub comments {
    my $entry = shift;
    my ($terms, $args) = @_;
    require MT::Comment;
    if ($terms || $args) {
        $terms ||= {};
        $terms->{entry_id} = $entry->id;
        return [ MT::Comment->load( $terms, $args ) ];
    } else {
        unless ($entry->{__comments}) {
            $entry->{__comments} = [ MT::Comment->load({
                entry_id => $entry->id
            }) ];
        }
        $entry->{__comments};
    }
}

sub comment_latest {
    my $entry = shift;
    unless ($entry->{__comment_latest}) {
        require MT::Comment;
        $entry->{__comment_latest} = MT::Comment->load({
            entry_id => $entry->id,
            visible => 1
        }, {
            'sort' => 'created_on',
            direction => 'descend',
            limit => 1,
        });
    }
    $entry->{__comment_latest};
}

sub comment_count {
    my $entry = shift;
    unless ($entry->{__comment_count}) {
        require MT::Comment;
        $entry->{__comment_count} = MT::Comment->count({
            entry_id => $entry->id,
            visible => 1
        });
    }
    $entry->{__comment_count};
}

sub pings {
    my $entry = shift;
    my ($terms, $args) = @_;
    if ($terms || $args) {
        $terms ||= {};
        $terms->{entry_id} = $entry->id;
        return [ MT::TBPing->load( $terms, $args ) ];
    } else {
        unless ($entry->{__pings}) {
            $entry->{__pings} = [ MT::TBPing->load({
                entry_id => $entry->id
            }) ];
        }
        $entry->{__pings};
    }
}

sub ping_count {
    my $entry = shift;
    unless ($entry->{__ping_count}) {
        require MT::Trackback;
        require MT::TBPing;
        my $tb = MT::Trackback->load({ entry_id => $entry->id });
        $entry->{__ping_count} = $tb ?
            MT::TBPing->count({ tb_id => $tb->id, visible => 1 }) : 0;
    }
    $entry->{__ping_count};
}

sub archive_file {
    my $entry = shift;
    my($at) = @_;
    my $blog = $entry->blog() || return $entry->error(MT->translate(
                                                     "Load of blog failed: [_1]",
                                                     MT::Blog->errstr));
    unless ($at) {
        $at = $blog->archive_type_preferred || $blog->archive_type;
        return '' if !$at || $at eq 'None';
        my %at = map { $_ => 1 } split /,/, $at;
        for my $tat (qw( Individual Daily Weekly Monthly Category )) {
            $at = $tat if $at{$tat};
        }
    }
    archive_file_for($entry, $blog, $at);
}

sub archive_url {
    my $entry = shift;
    my $blog = $entry->blog() || return $entry->error(MT->translate(
                                                     "Load of blog failed: [_1]",
                                                     MT::Blog->errstr));
    my $url = $blog->archive_url || "";
    $url .= '/' unless $url =~ m!/$!;
    $url . $entry->archive_file(@_);
}

sub permalink {
    my $entry = shift;
    my $blog = $entry->blog() || return $entry->error(MT->translate(
                                                     "Load of blog failed: [_1]",
                                                     MT::Blog->errstr));
    my $url = $entry->archive_url($_[0]);
    my $effective_archive_type = ($_[0]
        || $blog->archive_type_preferred
        || $blog->archive_type);
    $url .= '#' . ($_[1]->{valid_html} ? 'a' : '') . 
        sprintf("%06d", $entry->id)
        unless ($effective_archive_type eq 'Individual' 
        || $_[1]->{no_anchor});
    $url;
}

sub all_permalinks {
    my $entry = shift;
    my $blog = $entry->blog || return $entry->error(MT->translate(
                                                    "Load of blog failed: [_1]",
                                                    MT::Blog->errstr));
    my @at = split /,/, $blog->archive_type;
    return unless @at;
    my @urls;
    for my $at (@at) {
        push @urls, $entry->permalink($at);
    }
    @urls;
}

sub text_filters {
    my $entry = shift;
    my $filters = $entry->convert_breaks;
    if (!defined $filters) {
        my $blog = $entry->blog() || return [];
        $filters = $blog->convert_paras;
    }
    return [] unless $filters;
    if ($filters eq '1') {
        return [ '__default__' ];
    } else {
        return [ split /\s*,\s*/, $filters ];
    }
}

sub get_excerpt {
    my $entry = shift;
    my($words) = @_;
    return $entry->excerpt if $entry->excerpt;
    my $excerpt = MT->apply_text_filters($entry->text, $entry->text_filters);
    my $blog = $entry->blog() || return $entry->error(MT->translate(
                                                     "Load of blog failed: [_1]",
                                                     MT::Blog->errstr));
    MT::I18N::first_n_text($excerpt, $words || $blog->words_in_excerpt || MT::I18N::const('DEFAULT_LENGTH_ENTRY_EXCERPT')) . '...';
}

sub pinged_url_list {
    my $entry = shift;
    my (%param) = @_;
    my $include_failures = $param{Failures} || $param{OnlyFailures};
    my $exclude_successes = $param{OnlyFailures};
    my $urls = $entry->pinged_urls;
    return [] unless $urls && $urls =~ /\S/;
    my %urls = map { $_ => 1 } split /\r?\n/, $urls;
    my %to_ping = map { $_ => 1 } @{ $entry->to_ping_url_list };
    foreach (keys %to_ping) {
        delete $urls{$_} if exists $urls{$_};
    }
    my @urls = keys %urls;
    foreach (@urls) {
        if (m/^([^ ]+) /) {
            delete $urls{$_}; # remove ones with error messages
            $urls{$1} = 1 if $include_failures;
        } else {
            delete $urls{$_} if $exclude_successes;
        }
    }
    [ keys %urls ];
}

sub to_ping_url_list {
    my $entry = shift;
    my $urls = $entry->to_ping_urls;
    return [] unless $urls && $urls =~ /\S/;
    [ split /\r?\n/, $urls ];
}

# TBD: Write a test for this routine
sub make_atom_id {
    my $entry = shift;

    my $blog = $entry->blog;
    my ($host, $year, $path, $blog_id, $entry_id);
    $blog_id = $blog->id;
    $entry_id = $entry->id;
    my $url = $blog->site_url || '';
    return unless $url;
    $url .= '/' unless $url =~ m!/$!;
    if ($url && ($url =~ m!^https?://([^/:]+)(?::\d+)?(/.*)$!)) {
        $host = $1;
        $path = $2;
    }
    if ($entry->created_on && ($entry->created_on =~ m/^(\d{4})/)) {
        $year = $1;
    }
    return unless $host && $year && $path && $blog_id && $entry_id;
    qq{tag:$host,$year:$path/$blog_id.$entry_id};
}

sub discover_tb_from_entry {
    my $entry = shift;
    ## If we need to auto-discover TrackBack ping URLs, do that here.
    require MT::ConfigMgr;
    my $cfg = MT::ConfigMgr->instance;
    my $blog = $entry->blog();
    my $send_tb = $cfg->OutboundTrackbackLimit;
    if ($send_tb ne 'off' && 
        $blog && ($blog->autodiscover_links
                  || $blog->internal_autodiscovery)) {
        my @tb_domains;
        if ($send_tb eq 'selected') {
            @tb_domains = $cfg->OutboundTrackbackDomains;
        } elsif ($send_tb eq 'local') {
            my $iter = MT::Blog->load_iter();
            while (my $b = $iter->()) {
                next if $b->id == $blog->id;
                push @tb_domains, extract_domain($b->site_url);
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
        my $archive_domain;
        ($archive_domain) = extract_domains($blog->archive_url);
        my %to_ping = map { $_ => 1 } @{ $entry->to_ping_url_list };
        my %pinged = map { $_ => 1 } @{ $entry->pinged_url_list(IncludeFailures => 1) };
        my $body = $entry->text . ($entry->text_more || "");
        $body = MT->apply_text_filters($body, $entry->text_filters);
        while ($body =~ m!<a\s.*?\bhref\s*=\s*(["']?)([^'">]+)\1!gsi) {
            my $url = $2;
            my $url_domain;
            ($url_domain) = extract_domains($url);
            if ($url_domain =~ m/\Q$archive_domain\E$/i) {
                next if !$blog->internal_autodiscovery;
            } else {
                next if !$blog->autodiscover_links;
            }
            next if $tb_domains && lc($url_domain) !~ m/$tb_domains$/;
            if (my $item = discover_tb($url)) {
                $to_ping{ $item->{ping_url} } = 1
                    unless $pinged{$item->{ping_url}};
            }
        }
        $entry->to_ping_urls(join "\n", keys %to_ping);
    }
}

sub save {
    my $entry = shift;

    ## If there's no basename specified, create a unique basename.
    if (!defined($entry->basename) || ($entry->basename eq '')) {
        my $name = MT::Util::make_unique_basename($entry);
        $entry->basename($name);
    }
    if (my $dt = $entry->created_on_obj) {
        my ($yr, $w) = $dt->week;
        $entry->week_number($yr * 100 + $w);
    }

    unless ($entry->SUPER::save(@_)) {
        print STDERR "error during save: " . $entry->errstr . "\n";
        die $entry->errstr;
    }

    if (!$entry->atom_id && (($entry->status || 0) != HOLD)) {
        $entry->atom_id($entry->make_atom_id());
        $entry->SUPER::save(@_) if $entry->atom_id;
    }

    # synchronize tags if necessary
    $entry->save_tags;

    ## If pings are allowed on this entry, create or update
    ## the corresponding TrackBack object for this entry.
    require MT::Trackback;
    if ($entry->allow_pings) {
        my $tb;
        unless ($tb = $entry->trackback) {
            $tb = MT::Trackback->new;
            $tb->blog_id($entry->blog_id);
            $tb->entry_id($entry->id);
            $tb->category_id(0);   ## category_id can't be NULL
        }
        $tb->title($entry->title);
        $tb->description($entry->get_excerpt);
        $tb->url($entry->permalink);
        $tb->is_disabled(0);
        $tb->save
            or return $entry->error($tb->errstr);
        $entry->trackback($tb);
    } else {
        ## If there is a TrackBack item for this entry, but
        ## pings are now disabled, make sure that we mark the
        ## object as disabled.
        if (my $tb = MT::Trackback->load({ entry_id => $entry->id })) {
            $tb->is_disabled(1);
            $tb->save
                or return $entry->error($tb->errstr);
        }
    }

    delete $entry->{__next} if exists $entry->{__next};
    delete $entry->{__previous} if exists $entry->{__previous};

    1;
}

sub remove {
    my $entry = shift;

    my $comments = $entry->comments;
    $_->remove for @$comments;

    require MT::Placement;
    my @place = MT::Placement->load({ entry_id => $entry->id });
    $_->remove for @place;

    require MT::Trackback;
    my @tb = MT::Trackback->load({ entry_id => $entry->id });
    $_->remove for @tb;

    $entry->remove_tags;

    # Archive types other than Individual may refer to this entry, but
    # not essentially.  only the individual A.T. needs to be blottoed.
    require MT::FileInfo;
    my @finfos = MT::FileInfo->load({
        entry_id => $entry->id,
        archive_type => 'Individual',
    });
    $_->remove for @finfos;

    $entry->SUPER::remove;
}

sub blog {
    my ($entry) = @_;
    my $blog = $entry->{__blog};
    unless ($blog) {
        my $blog_id = $entry->blog_id;
        require MT::Blog;
        $blog = MT::Blog->load($blog_id, {cached_ok=>1}) or
            return $entry->error(MT->translate(
                                 "Load of blog '[_1]' failed: [_2]", $blog_id, MT::Blog->errstr));
        $entry->{__blog} = $blog;
    }
    return $blog;
}

sub to_hash {
    my $entry = shift;
    my $hash = $entry->SUPER::to_hash(@_);

    $hash->{'entry.text_html'} = sub { MT->apply_text_filters($entry->text, $entry->text_filters) };
    $hash->{'entry.text_more_html'} = sub { MT->apply_text_filters($entry->text_more, $entry->text_filters) };
    $hash->{'entry.permalink'} = $entry->permalink;
    $hash->{'entry.status_text'} = $entry->status_text;
    $hash->{'entry.status_is_' . $entry->status} = 1;
    $hash->{'entry.created_on_iso'} = sub { MT::Util::ts2iso($entry->blog_id, $entry->created_on) };
    $hash->{'entry.modified_on_iso'} = sub { MT::Util::ts2iso($entry->blog_id, $entry->modified_on) };

    # Populate author info
    my $auth = $entry->author or return $hash;
    my $auth_hash = $auth->to_hash;
    $hash->{"entry.$_"} = $auth_hash->{$_} foreach keys %$auth_hash;

    $hash;
}

1;
__END__

=head1 NAME

MT::Entry - Movable Type entry record

=head1 SYNOPSIS

    use MT::Entry;
    my $entry = MT::Entry->new;
    $entry->blog_id($blog->id);
    $entry->status(MT::Entry::RELEASE());
    $entry->author_id($author->id);
    $entry->title('My title');
    $entry->text('Some text');
    $entry->save
        or die $entry->errstr;

=head1 DESCRIPTION

An I<MT::Entry> object represents an entry in the Movable Type system. It
contains all of the metadata about the entry (author, status, category, etc.),
as well as the actual body (and extended body) of the entry.

=head1 USAGE

As a subclass of I<MT::Object>, I<MT::Entry> inherits all of the
data-management and -storage methods from that class; thus you should look
at the I<MT::Object> documentation for details about creating a new object,
loading an existing object, saving an object, etc.

The following methods are unique to the I<MT::Entry> interface:

=head2 $entry->next

Loads and returns the next entry, where "next" is defined as the next record
in ascending chronological order (the entry posted after the current entry).
entry I<$entry>).

Returns an I<MT::Entry> object representing this next entry; if there is not
a next entry, returns C<undef>.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->previous

Loads and returns the previous entry, where "previous" is defined as the
previous record in ascending chronological order (the entry posted before the
current entry I<$entry>).

Returns an I<MT::Entry> object representing this previous entry; if there is
not a next entry, returns C<undef>.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->author

Returns an I<MT::Author> object representing the author of the entry
I<$entry>. If the author record has been removed, returns C<undef>.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->category

Returns an I<MT::Category> object representing the primary category of the
entry I<$entry>. If a primary category has not been assigned, returns
C<undef>.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->categories

Returns a reference to an array of I<MT::Category> objects representing the
categories to which the entry I<$entry> has been assigned (both primary and
secondary categories). If the entry has not been assigned to any categories,
returns a reference to an empty array.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->is_in_category($cat)

Returns true if the entry I<$entry> has been assigned to entry I<$cat>, false
otherwise.

=head2 $entry->comments

Returns a reference to an array of I<MT::Comment> objects representing the
comments made on the entry I<$entry>. If no comments have been made on the
entry, returns a reference to an empty array.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->comment_count

Returns the number of comments made on this entry.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->ping_count

Returns the number of TrackBack pings made on this entry.

Caches the return value internally so that subsequent calls will not have to
re-query the database.

=head2 $entry->archive_file([ $archive_type ])

Returns the name of/path to the archive file for the entry I<$entry>. If
I<$archive_type> is not specified, and you are using multiple archive types
for your blog, the path is created from the preferred archive type that you
have selected. If I<$archive_type> is specified, it should be one of the
following values: C<Individual>, C<Daily>, C<Weekly>, C<Monthly>, and
C<Category>.

=head2 $entry->archive_url([ $archive_type ])

Returns the absolute URL to the archive page for the entry I<$entry>. This
calls I<archive_file> internally, so if I<$archive_type> is specified, it
is merely passed through to that method. In other words, this is the
blog Archive URL plus the results of I<archive_file>.

=head2 $entry->permalink([ $archive_type ])

Returns the (smart) permalink for the entry I<$entry>. Internally this calls
I<archive_url>, which calls I<archive_file>, so I<$archive_type> (if
specified) is merely passed through to that method. The result of this
method is the same as I<archive_url> plus the URI fragment
(C<#entry_id>), unless the preferred archive type is Individual, in which
case the two methods give exactly the same results.

=head2 $entry->text_filters

Returns a reference to an array of text filter keynames (the short names
that are the first argument to I<MT::add_text_filter>. This list can be
passed directly in as the second argument to I<MT::apply_text_filters>.

=head1 DATA ACCESS METHODS

The I<MT::Entry> object holds the following pieces of data. These fields can
be accessed and set using the standard data access methods described in the
I<MT::Object> documentation.

=over 4

=item * id

The numeric ID of the entry.

=item * blog_id

The numeric ID of the blog in which this entry has been posted.

=item * author_id

The numeric ID of the author who posted this entry.

=item * status

The status of the entry, either Publish (C<2>) or Draft (C<1>).

=item * allow_comments

An integer flag specifying whether comments are allowed on this entry. This
setting determines whether C<E<lt>MTEntryIfAllowCommentsE<gt>> containers are
displayed for this entry. Possible values are 0 for no comments, 1 for open
comments and 2 for closed comments (that is, display the comments on this
entry but do not allow new comments to be added).

=item * convert_breaks

A boolean flag specifying whether line and paragraph breaks should be converted
when rebuilding this entry.

=item * title

The title of the entry.

=item * excerpt

The excerpt of the entry.

=item * text

The main body text of the entry.

=item * text_more

The extended body text of the entry.

=item * created_on

The timestamp denoting when the entry record was created, in the format
C<YYYYMMDDHHMMSS>. Note that the timestamp has already been adjusted for the
selected timezone.

=item * modified_on

The timestamp denoting when the entry record was last modified, in the
format C<YYYYMMDDHHMMSS>. Note that the timestamp has already been adjusted
for the selected timezone.

=back

=head1 DATA LOOKUP

In addition to numeric ID lookup, you can look up or sort records by any
combination of the following fields. See the I<load> documentation in
I<MT::Object> for more information.

=over 4

=item * blog_id

=item * status

=item * author_id

=item * created_on

=item * modified_on

=back

=head1 NOTES

=over 4

=item *

When you remove an entry using I<MT::Entry::remove>, in addition to removing
the entry record, all of the comments and placements (I<MT::Comment> and
I<MT::Placement> records, respectively) for this entry will also be removed.

=back

=head1 AUTHOR & COPYRIGHTS

Please see the I<MT> manpage for author, copyright, and license information.

=cut
