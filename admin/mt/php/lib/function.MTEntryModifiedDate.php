<?php
function smarty_function_MTEntryModifiedDate($args, &$ctx) {
    $entry = $ctx->stash('entry');
    $args['ts'] = $entry['entry_modified_on'];
    return $ctx->_hdlr_date($args, $ctx);
}
?>
