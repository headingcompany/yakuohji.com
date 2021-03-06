# Copyright 2001-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.  For more information, consult your
# Movable Type license.
#
# $Id: Config.pm 2 2006-06-09 23:16:03Z hachi $

package MT::Config;
use strict;

use MT::Object;
@MT::Config::ISA = qw( MT::Object );
__PACKAGE__->install_properties({
    column_defs => {
        'id' => 'integer not null auto_increment',
        'data' => 'text',
    },
    primary_key => 'id',
    datasource => 'config',
});

1;

__END__

=pod

=head1 NAME

MT::Config - Installation-wide configuration data.

=cut
