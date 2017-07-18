// Informal source: https://quilljs.com/guides/cloning-medium-with-parchment/

// Global import
let Parchment = Quill.import("parchment");

// Default block
class Block extends Quill.import("blots/block")
{
    static create(value)
    {
        let node = super.create(value);
        node.setAttribute("class", "vitxt-paragraph");
        return node;
    }
}

Quill.register(Block, true);

// Bold
class BoldBlot extends Quill.import("formats/bold")
{
    static create(value)
    {
        let node = super.create(value);
        node.setAttribute("class", "vitxt-fBold");
        return node;
    }
}

BoldBlot.blotName = "bold";
BoldBlot.tagName = "strong";

Quill.register(BoldBlot, true);

// Italic
class ItalicBlot extends Quill.import("formats/italic")
{
    static create(value)
    {
        let node = super.create(value);
        node.setAttribute("class", "vitxt-fItalic");
        return node;
    }
}

ItalicBlot.blotName = "italic";
ItalicBlot.tagName = "em";

Quill.register(ItalicBlot, true);



// Super & Sub
class SuperSubBlot extends Quill.import("blots/inline")
{
    static create(value)
    {
        if (value == "Super")
        {
            SuperSubBlot.tagName = "sup";
        }
        else if (value == "Sub")
        {
            SuperSubBlot.tagName = "sub";
        }

        let node = super.create(value);
        node.setAttribute("class", "vitxt-f" + value);
        
        return node;
    }
}

SuperSubBlot.blotName = "subsuper";

Quill.register(SuperSubBlot, true);

// Blockquote
class BlockquoteBlot extends Quill.import("formats/blockquote")
{
    static create(value)
    {
        let node = super.create(value);
        node.setAttribute("class", "vitxt-tQuote");
        return node;
    }
}

Quill.register(BlockquoteBlot, true);

// Header
class HeaderBlot extends Quill.import("formats/header")
{
    static create(value)
    {
        let cl = {
            1: "title",
            2: "large",
            3: "medium",
            4: "small",
        };

        let node = super.create(value);
        node.setAttribute("class", "vitxt-tHeading vitxt-tHeading-" + cl[value]);
        return node;
    }
}

HeaderBlot.blotName = "header";
HeaderBlot.tagName = ["h1", "h2", "h3", "h4"];
Quill.register(HeaderBlot, true);

// Align
let alignOptions = { scope: Parchment.Scope.BLOCK, whitelist: ["Left", "Right", "Center", "Justify"] };
let AlignClass = new Parchment.Attributor.Class("align", "vitxt-a", alignOptions);
Quill.register({"attributors/class/align": AlignClass,
                "formats/align": AlignClass}, true);


// List
class ListBlot extends Quill.import("formats/list")
{
    static create(value)
    {
        let node = super.create(value);
        if (value == "ordered")
        {
            node.setAttribute("class", "vitxt-list vitxt-listOrder");
        }
        else if (value == "bullet")
        {
            node.setAttribute("class", "vitxt-list vitxt-listUnorder");
        }

        return node;
    }
}

Quill.register(ListBlot, true);

// List Item
class ListItemBlot extends Quill.import("formats/list/item")
{
    static create(value)
    {
        let node = super.create(value);
        node.setAttribute("class", "vitxt-listItem");

        return node;
    }
}

Quill.register(ListItemBlot, true);


// Indent
class IndentBlot extends Quill.import("blots/block")
{
    static create(value)
    {
        let node = super.create(value);
        node.setAttribute("class", "vitxt-indent");
        return node;
    }
}

IndentBlot.blotName = "indent";
IndentBlot.tagName = "div";

Quill.register(IndentBlot, true);