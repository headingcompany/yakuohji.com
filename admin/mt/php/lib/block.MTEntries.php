<?php
function smarty_block_MTEntries($args, $content, &$ctx, &$repeat) {
    $localvars = array('entry', '_entries_counter','entries','current_timestamp','modification_timestamp','_entries_lastn', 'current_timestamp_end', 'DateHeader', 'DateFooter', '_entries_glue');
    if (!isset($content)) {
        $ctx->localize($localvars);
        // If we have a set of entries that were set based on context,
        // but the user has specified attributes that effectively
        // break that context, clear the stashed entries so fetch_entries
        // can reselect.
        if ($ctx->stash('entries') &&
            (isset($args['category']) || isset($args['categories']) ||
             isset($args['tag']) || isset($args['tags']) ||
             isset($args['author']) ||
             isset($args['recently_commented_on']) ||
             isset($args['include_subcategories']) ||
             isset($args['days']) ))
            $ctx->__stash['entries'] = null;
        $counter = 0;
        $lastn = $args['lastn'];
        $ctx->stash('_entries_lastn', $lastn);
    } else {
        $lastn = $ctx->stash('_entries_lastn');
        $counter = $ctx->stash('_entries_counter');
    }
    $entries = $ctx->stash('entries');
    if (!isset($entries)) {
        $args['blog_id'] = $ctx->stash('blog_id');
        if ($at = $ctx->stash('current_archive_type')) {
            $args['lastn'] or $args['lastn'] = -1;
            $ts = $ctx->stash('current_timestamp');
            $tse = $ctx->stash('current_timestamp_end');
            global $_archive_helpers;
            if (($ts && $tse) && isset($_archive_helpers[$at])) {
                # assign date range if we have both
                # start and end date
                $args['current_timestamp'] = $ts;
                $args['current_timestamp_end'] = $tse;
            }
        }
        if ($cat = $ctx->stash('category')) {
            $args['category'] or $args['categories'] or $args['category_id'] = $cat['category_id'];
        }
        if ($tag = $ctx->stash('Tag')) {
            $args['tag'] or $args['tags'] or $args['tags'] = is_array($tag) ? $tag['tag_name'] : $tag;
        }
        $entries =& $ctx->mt->db->fetch_entries($args);
        $ctx->stash('entries', $entries);
    }
    $ctx->stash('_entries_glue', $args['glue']);
    if (($lastn > count($entries)) || ($lastn == -1)) {
        $lastn = count($entries);
        $ctx->stash('_entries_lastn', $lastn);
    }
    if ($lastn ? ($counter < $lastn) : ($counter < count($entries))) {
        $entry = $entries[$counter];
        if ($counter > 0) {
            $last_entry_created_on = $entries[$counter-1]['entry_created_on'];
        } else {
            $last_entry_created_on = '';
        }
        if ($counter < count($entries)-1) {
            $next_entry_created_on = $entries[$counter+1]['entry_created_on'];
        } else {
            $next_entry_created_on = '';
        }
        $ctx->stash('DateHeader', !(substr($entry['entry_created_on'], 0, 8) == substr($last_entry_created_on, 0, 8)));
        $ctx->stash('DateFooter', (substr($entry['entry_created_on'], 0, 8) != substr($next_entry_created_on, 0, 8)));
        $ctx->stash('entry', $entry);
        $ctx->stash('current_timestamp', $entry['entry_created_on']);
        $ctx->stash('current_timestamp_end', null);
        $ctx->stash('modification_timestamp', $entry['entry_modified_on']);
        $ctx->stash('_entries_counter', $counter + 1);
        $glue = $ctx->stash('_entries_glue');
        if ($glue != '') $content = $content . $glue;
        $repeat = true;
    } else {
        $ctx->restore($localvars);
        $repeat = false;
    }
    return $content;
}
?>
