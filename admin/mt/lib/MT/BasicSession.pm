package MT::BasicSession;

# fake out the require for this package since we're
# declaring it inline...

use MT::Object;
@MT::BasicSession::ISA = qw( MT::Object );
__PACKAGE__->install_properties({
    column_defs => {
        'id' => 'string(80) not null primary key',
        'data' => 'blob',
        'email' => 'string(255)',
        'name' => 'string(255)',
        'kind' => 'string(2)',
        'start' => 'integer not null',
    },
    indexes => {
        'start' => 1,
        'kind' => 1
    },
    datasource => 'session',
});

# sub load {
#     SUPER::load(@_) or return undef;
# }

1;
