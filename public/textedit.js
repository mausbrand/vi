"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// Informal source: https://quilljs.com/guides/cloning-medium-with-parchment/

// Global import
var Parchment = Quill.import("parchment");

// Default block

var Block = function (_Quill$import) {
    _inherits(Block, _Quill$import);

    function Block() {
        _classCallCheck(this, Block);

        return _possibleConstructorReturn(this, (Block.__proto__ || Object.getPrototypeOf(Block)).apply(this, arguments));
    }

    _createClass(Block, null, [{
        key: "create",
        value: function create(value) {
            var node = _get(Block.__proto__ || Object.getPrototypeOf(Block), "create", this).call(this, value);
            node.setAttribute("class", "vitxt-paragraph");
            return node;
        }
    }]);

    return Block;
}(Quill.import("blots/block"));

Quill.register(Block, true);

// Bold

var BoldBlot = function (_Quill$import2) {
    _inherits(BoldBlot, _Quill$import2);

    function BoldBlot() {
        _classCallCheck(this, BoldBlot);

        return _possibleConstructorReturn(this, (BoldBlot.__proto__ || Object.getPrototypeOf(BoldBlot)).apply(this, arguments));
    }

    _createClass(BoldBlot, null, [{
        key: "create",
        value: function create(value) {
            var node = _get(BoldBlot.__proto__ || Object.getPrototypeOf(BoldBlot), "create", this).call(this, value);
            node.setAttribute("class", "vitxt-fBold");
            return node;
        }
    }]);

    return BoldBlot;
}(Quill.import("formats/bold"));

BoldBlot.blotName = "bold";
BoldBlot.tagName = "strong";

Quill.register(BoldBlot, true);

// Italic

var ItalicBlot = function (_Quill$import3) {
    _inherits(ItalicBlot, _Quill$import3);

    function ItalicBlot() {
        _classCallCheck(this, ItalicBlot);

        return _possibleConstructorReturn(this, (ItalicBlot.__proto__ || Object.getPrototypeOf(ItalicBlot)).apply(this, arguments));
    }

    _createClass(ItalicBlot, null, [{
        key: "create",
        value: function create(value) {
            var node = _get(ItalicBlot.__proto__ || Object.getPrototypeOf(ItalicBlot), "create", this).call(this, value);
            node.setAttribute("class", "vitxt-fItalic");
            return node;
        }
    }]);

    return ItalicBlot;
}(Quill.import("formats/italic"));

ItalicBlot.blotName = "italic";
ItalicBlot.tagName = "em";

Quill.register(ItalicBlot, true);

// Blockquote

var BlockquoteBlot = function (_Quill$import4) {
    _inherits(BlockquoteBlot, _Quill$import4);

    function BlockquoteBlot() {
        _classCallCheck(this, BlockquoteBlot);

        return _possibleConstructorReturn(this, (BlockquoteBlot.__proto__ || Object.getPrototypeOf(BlockquoteBlot)).apply(this, arguments));
    }

    _createClass(BlockquoteBlot, null, [{
        key: "create",
        value: function create(value) {
            var node = _get(BlockquoteBlot.__proto__ || Object.getPrototypeOf(BlockquoteBlot), "create", this).call(this, value);
            node.setAttribute("class", "vitxt-tQuote");
            return node;
        }
    }]);

    return BlockquoteBlot;
}(Quill.import("formats/blockquote"));

Quill.register(BlockquoteBlot, true);

// Header

var HeaderBlot = function (_Quill$import5) {
    _inherits(HeaderBlot, _Quill$import5);

    function HeaderBlot() {
        _classCallCheck(this, HeaderBlot);

        return _possibleConstructorReturn(this, (HeaderBlot.__proto__ || Object.getPrototypeOf(HeaderBlot)).apply(this, arguments));
    }

    _createClass(HeaderBlot, null, [{
        key: "create",
        value: function create(value) {
            var cl = {
                1: "title",
                2: "large",
                3: "medium",
                4: "small"
            };

            var node = _get(HeaderBlot.__proto__ || Object.getPrototypeOf(HeaderBlot), "create", this).call(this, value);
            node.setAttribute("class", "vitxt-tHeading vitxt-tHeading-" + cl[value]);
            return node;
        }
    }]);

    return HeaderBlot;
}(Quill.import("formats/header"));

HeaderBlot.blotName = "header";
HeaderBlot.tagName = ["h1", "h2", "h3", "h4"];
Quill.register(HeaderBlot, true);

// Align
var alignOptions = { scope: Parchment.Scope.BLOCK, whitelist: ["Left", "Right", "Center", "Justify"] };
var AlignClass = new Parchment.Attributor.Class("align", "vitxt-a", alignOptions);
Quill.register({ "attributors/class/align": AlignClass,
    "formats/align": AlignClass }, true);
