/**
 * @license Copyright (c) 2003-2022, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	CKEDITOR.on('instanceReady', function (ev) {
    ev.editor.dataProcessor.htmlFilter.addRules({
        elements: {
            img: function (element) {
                element.attributes.style = (element.attributes.style || '') + ';max-width: 100%;height: auto;';
            }
        }
    });
});
};
