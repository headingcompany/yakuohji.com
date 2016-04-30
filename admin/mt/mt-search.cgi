#!/usr/bin/perl -w

# Original copyright 2001-2002 Jay Allen.
# Modifications and integration Copyright 2001-2006 Six Apart.
# Copyright 2001-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.  For more information, consult your
# Movable Type license.
#
# $Id: mt-search.cgi 2 2006-06-09 23:16:03Z hachi $

use strict;
use lib $ENV{MT_HOME} ? "$ENV{MT_HOME}/lib" : 'lib';
use MT::Bootstrap App => 'MT::App::Search';
