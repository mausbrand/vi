// Informal source: https://quilljs.com/guides/cloning-medium-with-parchment/

var Parchment = Quill.import("parchment");

// Bold
var BoldBlot = Quill.import("formats/bold");
BoldBlot.blotName = "bold";
BoldBlot.tagName = "strong";
Quill.register(BoldBlot, true);

// Italic
var ItalicBlot = Quill.import("formats/italic");
ItalicBlot.blotName = "italic";
ItalicBlot.tagName = "em";
Quill.register(ItalicBlot, true);

// Blockquote
var BlockquoteBlot = Quill.import("formats/blockquote");
Quill.register(BlockquoteBlot, true);

// Header
var HeaderBlot = Quill.import("formats/header");
HeaderBlot.blotName = "header";
HeaderBlot.tagName = ["h1", "h2", "h3", "h4", "h5"];
Quill.register(HeaderBlot, true);

// Align
var alignOptions = { scope: Parchment.Scope.BLOCK, whitelist: ["right", "center"] };
var AlignClass = new Parchment.Attributor.Class("align", "vi-special", alignOptions);
Quill.register({"attributors/class/align": AlignClass,
                "formats/align": AlignClass}, true);
