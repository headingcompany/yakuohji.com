<?php
function smarty_block_MTCategoryNext($args, $content, &$ctx, &$repeat) {
    $localvars = array('category', 'entries');
    $tag = $ctx->this_tag();
    if ($tag == 'MTCategoryPrevious') {
        $step = -1;
    } else {
        $step = 1;
    }

    if (!isset($content)) {
        $e = $ctx->stash('entry');
        if ($e) $cat = $ctx->mt->db->fetch_category($e['placement_category_id']);
        $cat or $cat = $ctx->stash('category');
        $cat or $cat = $ctx->stash('archive_category');
        if (!$cat) return '';
        $needs_entries = $args['entries'];
        $cats = _catx_load_categories($ctx, $cat);
        $idx = 0;
        foreach ($cats as $c) {
            if ($c['category_id'] == $cat['category_id']) {
                $pos = $idx;
                break;
            }
            $idx++;
        }
        $repeat = false;
        if (isset($pos)) {
            $pos += $step;
            while (($pos >= 0) && ($pos < count($cats))) {
                if ($cats[$pos]['category_count'] == 0) {
                    if (isset($args['show_empty']) && $args['show_empty']) {
                    } else {
                        $pos += $step;
                        continue;
                    }
                }
                $ctx->localize($localvars);
                $ctx->stash('category', $cats[$pos]);
                if ($needs_entries) $ctx->stash('entries', null);
                $repeat = true;
                break;
            }
        }
    } else {
        $ctx->restore($localvars);
    }
    return $content;
}

function _catx_load_categories(&$ctx, $cat) {
    $blog_id = $cat['category_blog_id'];
    $parent = $cat['category_parent'];
    $parent or $parent = 0;
    $cats = $ctx->stash('__cat_cache_'.$blog_id . '_' . $parent);
    if (!$cats) {
        $cats = $ctx->mt->db->fetch_categories(array('blog_id' => $blog_id, 'parent' => $parent, 'show_empty' => 1));
        $ctx->stash('__cat_cache_'.$blog_id. '_' . $parent, $cats);
    }
    return $cats;
}
?>
