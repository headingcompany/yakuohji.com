# Copyright 2001-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.  For more details, consult 
# your Movable Type license for details.
#
# $Id: default-templates.pl 2 2006-06-09 23:16:03Z hachi $

package MT::default_templates;

use strict;
require MT::DefaultTemplates;

delete $INC{'MT/default-templates.pl'};

MT::DefaultTemplates->templates;
