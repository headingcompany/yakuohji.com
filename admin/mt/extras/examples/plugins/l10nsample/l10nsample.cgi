#!/usr/bin/perl -w

# Copyright 2005-2006 Six Apart. This code cannot be redistributed without
# permission from www.sixapart.com.
#
# $Id: l10nsample.cgi 2 2006-06-09 23:16:03Z hachi $

use strict;
use lib "lib", ($ENV{MT_HOME} ? "$ENV{MT_HOME}/lib" : "../../lib"); 
use MT::Bootstrap App => 'l10nsample';
