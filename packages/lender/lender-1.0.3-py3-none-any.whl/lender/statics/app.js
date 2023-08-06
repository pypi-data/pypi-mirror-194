// 硬核

// 周控制变量
// 0 当前周
// -1 上周
var CURRENT_WEEK = 0;

// true 修改了
// false 没修改
var EDITED_LOCK = false;


var EDITOR_PLACEHOLDER = [
    "当你为错过太阳而流泪，你也将错过群星了。",
    "天空虽不曾留下痕迹，但我已飞过。",
    "我们的生命是天赋的，我们惟有献出生命，才能得到生命。",
    "让生命有如夏花之绚烂，死亡有如秋叶之静美。",
    "爱是亘古长明的灯塔，它定晴望着风暴却兀不为动，爱就是充实了的生命，正如盛满了酒的酒杯。",
    "爱情是理解和体贴的别名。",
    "夜把花悄悄地开放了，却让白日去领受谢词。",
    "我希望你照自己的意思去理解自己，不要小看自己，被别人的意见引入歧途。",
    "妥协对任何友谊都不是坚固的基础。",
    "相信爱情，即使它给你带来悲哀也要相信爱情。",
    "错误经不起失败，但是真理却不怕失败。",
    "女人，罪恶把你剥得赤裸，诅咒把你洗净，你升华成完善的生命。",
    "你若爱她，让你的爱像阳光一样包围她，并且给她自由。",
    "你可以从外表的美来评论一朵花或一只蝴蝶，但你不能这样来评论一个人。",
    "我们只有献出生命，才能得到生命。",
    "在消除贫困的时候，我们会拥有自己的财富，而拥有这笔财富，我们却会失去多少善心，多少美和多少力量啊！",
    "静止便是死亡，只有运动才能敲开永生的大门。",
    "老是考虑怎样去做好事的人，就没有时间去做好事。",
    "闪射理想之光吧，心灵之星！把光流注入，未来的暮霭之中。",
    "信仰是个鸟儿，黎明还是黝黑时，就触着曙光而讴歌了。",
    "果实的事业是尊贵的，花的事业是甜美的，但是让我们做叶的事业罢，叶是谦逊地专心地垂着绿荫的。",
    "月儿把她的光明遍照在天上，却留着她的黑斑给它自己。",
    "人走到喧华的群众中去，是为了淹没他自己沉默的呼号。",
    "真理之川从他的错误的沟渠中流过。",
    "在光明中高举，在死的阴影里把它收起。和你的星星一同放进夜的宝盒，早晨，让它在礼拜声中开放的鲜花丛里找到它自己。",
    "如果把所有的错误都关在门外的话，真理也要被关在门外了。",
    "真理之川从他的错误之沟渠中通过。",
    "有生命力的理想决不能象钟表一样，精确计算它的每一秒钟。",
    "永恒的献身是生命的真理。它的完美就是我们生命的完美。",
    "生活不是局限于人类追求自己的实际目标所进行的日常行动，而是显示了人类参加到一种宇宙韵律中来，这种韵律以形形色色的方式证明其自身的存在。",
    "世界上的一切伟大运动都与某种伟大理想有关。",
    "生命是永恒不断的创造，因为在它内部蕴含着过剩的精力，它不断流溢，越出时间和空间的界限，它不停地追求，以形形色色的自我表现的形式表现出来。",
    "界上使社会变得伟大的人，正是那些有勇气在生活中尝试和解决人生新问题的人！",
    "蜜蜂从花中啜蜜，离开时营营的道谢。浮夸的蝴蝶却相信花是应该向他道谢的。",
    "不要从你自己的袋里掏出勋章借给你的朋友，这是侮辱他的。",
    "我愿我能在横过孩子心中的道路上游行，解脱了一切的束缚；……在那儿，理智以它的法律造为纸鸢而飞放，真理也使事实从桎梏中自由了。",
    "真理是严酷的，我喜爱这个严酷，它永不欺骗。",
    "当我们是大为谦卑的时候，便是我们最近于伟大的时候。",
    "友谊和爱情之间的区别在于：友谊意味着两个人和世界，然而爱情意味着两个人就是世界。在友谊中一加一等于二；在爱情中一加一还是一。",
    "我们热爱这个世界时，才真正活在这个世界上。",
    "检验真理的工作也没有被过去某一个时代的一批学者一一劳永逸地完成；真理必须通过它在各个时代受到的反对和打击被人重新发展。",
    "休息与工作的关系，正如眼睑与眼睛的关系。",
    "人生虽只有几十春秋，但它决不是梦一般的幻灭，而是有着无穷可歌可颂的深长意义的；附和真理，生命便会得到永生。",
    "青春啊，难道你始终囚禁在狭小圈子里？你得撕破老年的蛊惑人心的网。",
    "青春是没有经验和任性的。",
    "当青春的光彩渐渐消逝，永不衰老的内在个性却在一个人的脸上和眼睛上更加明显地表露出来，好像是在同一地方久住了的`结果。",
    "人的青春时期一过，就会出现名象秋天一样的优美成熟时期，这时，生命的果实象熟稻子似的在美丽的平静的气氛中等待收获。",
    "有些事情是不能等待的。假如你必须战斗或者在市场上取得最有利的地位，你就不能不冲锋、奔跑和大步行进。",
    "造物主把像你这样的人派遣到人世间来，是要你担负一定的责任的，所以你决不应该轻视自己的身体。",
    "年轻时，我的生命有如一朵花。",
    "只有人类精神能够蔑视一切限制，想信它的最后成功，将它的探照灯照向黑暗的远方。",
    "埋在地下的树根使树枝产生果实，却并不要求什么报酬。",
    "他把他的刀剑当做他的上帝。当他的刀剑胜利时，他自己却失败了。",
    "梦是一个一定要谈话的妻子，睡眠是一个默默忍受的丈夫。",
    "知识是珍贵宝石的结晶，文化是宝石放出的光泽。",
    "在你青春的无忧无虑的生涯里，你屋子里所有的门户始终洞开着。",
    "一个人的青春时期一过，就会出现像秋天一样的优美的成熟时期，这时，生命的果实像熟稻子似的在美丽的平静的气氛中等待收获。",
    "在老年时，会有许多闲暇的时间，去计算那过去的日子，把我们手里永久丢失了的东西，在心里爱抚着。",
    "人总是要犯错误、受挫折、伤脑筋的，不过决不能停滞不前；应该完成的任务，即使为它牺牲生命，也要完成。",
    "社会之河的圣水就是因为被一股永不停滞的激流推动向前才得以保持洁净。",
    "我更需要的是给与，不是收受。因为爱是一个流浪者他能使他的花朵在道旁的泥土里蓬勃焕发，却不容易叫它们在会客室的水晶瓶里尽情开放。",
    "时间是变化的财富。时钟模仿它，却只有变化而无财富。",
    "任何事物都无法抗拒吞食一切的时间。",
    "要是童年的日子能重新回来，那我一定不再浪费光阴，我要把每分每秒都用来读书！",
    "有勇气在自己生活中尝试解决人生新问题的人，正是那些使社会臻于伟大的人！",
    "多和朋辈交游无疑是医治心病的良方。",
    "不要从你自己的袋里掏出勋绩借给你的朋友，这是污辱他的。",
    "有时候，两个从不相识的人的确也很可能一见面就变成了知心的朋友。",
    "花朵以芬芳熏香了空气，但它的最终任务，是把自己献给你。",
    "在哪里找到了朋友，我就在哪里重生。",
    "那些缠扭着家庭的人，命定要永远闭卧在无灵魂世界的僵硬的生活中。",
    "思想以自己的言语喂养它自己，而成长起来。",
    "全是理智的心，恰如一柄全是锋刃的刀。它叫使用它的人手上流血。",
    "学习必须与实干相结合。",
    "最好的东西都不是独来的，它伴了所有的东西同来。",
    "阴影戴上她的面幕，秘密地，温顺地，用她的沉默的爱的脚步，跟在“光”后边。",
    "不要试图去填满生命的空白，因为，音乐就来自那空白深处。",
    "我的存在，是一个永久的惊奇，而这，就是人生。",
    "有一次，我们梦见彼此竟是陌生人；醒来后，才发现我们原是相亲相爱的。",
    "鸟儿愿为一朵云，云儿愿为一只鸟。",
    "不要因为你胃口不好，而抱怨你的食物。",
    "你默默微笑着，不对我说一句话，但我感觉，为了这个，我已期待很久了。",
    "我们辨识错了世界，却说世界欺骗了我们。",
    "为什么为了给记忆建筑这样多的神龛而消磨生命呢？这是徒劳无益的。你不知道，生命是在死亡的神坛上永恒的牺牲品吗？",
    "祭司的念珠和警察的鞭子是用同一种绳子串起来的。",
    "爱情若被束缚，世人的旅程即刻中止。爱情若葬入坟墓，旅人就是倒在坟上的墓碑。",
    "我宁愿要那种虽然看不见但表现出内在品质的美。",
    "要是爱情不允许彼此之间有所差异，那么为什么世界上到处都有差异呢？",
    "快乐很简单，但要做到简单却很难。",
    "我听见回声，来自山谷和心间 以寂寞的镰刀收割空旷的灵魂 不断地重复决绝，又重复幸福 终有绿洲摇曳在沙漠",
    "生如夏花之绚烂， 死如秋叶之静美。 笑看红尘之憾叹， 莫哭人生之悲哀。",
    "只管走过去，不要逗留着去采了花朵来保存，因为一路上，花朵会继续开放的。",
    "静夜有母亲的美丽，如喧哗的白日之于孩子。",
    "我的心是旷野的鸟，在你的眼睛里找到了它的天空。",
    "打开门，让蓝天没有阻挡地泻进来，让花的芬芳香进我的房间。",
    "我给你爱的阳光，同时给你光辉灿烂的自由。",
    "静听，我的心。 他的笛声， 就是野花的气息的音乐， 闪亮的树叶、光耀的流水的音乐， 影子回响着蜜蜂之翼的音乐。 笛声从我朋友的唇上，偷走了微笑，把这微笑蔓延在我的生命上。",
    "我的心张开帆 借着无所事事的风 去无所谓哪里的岛",
    "让死者有那不朽的名，但让生者有那不朽的爱。",
    "总有一天，我要在别的世界的晨光里对你唱道：“我以前在地球的光里，在人的爱里，已经见过你。",
    "我将一次又一次的死去，以此来证明生命的无穷的，我相信自己 生来如同璀璨的夏日之花 不凋不败，妖冶如火",
    "对于你，这里没有希望，没有恐怖。 这里没有消息，没有低语，没有呼唤。 这里没有休息的床。 这里只有你自己的一双翅膀和无路的天空。",
    "世界上最远的距离，不是，彼此相爱，却不能够在一起，而是，明明无法抵挡这一股气息，却装作毫不在意！",
    "青春的精神是点铁成金的奇异的宝石。",
    "天空没有留下鸟的痕迹，但我已飞过。",
    "不好试图去填满生命的空白，正因，音乐就来自那空白深处。爱情过后",
    "人世间，欢乐与忧愁，机遇与不幸，疑虑与危险，以及绝望与悔恨总是混杂在一起的。",
    "一个全是逻辑的头脑，恰如一柄全是锋刃的刀。它令使用这刀的手流血！",
    "今天大地在太阳光里向我营营哼鸣，象一个织着布的妇人，用一种已经被忘却的语言，哼着一些古代的歌曲。",
    "天刚破晓，我就驱车起行，穿遍广漠的世界，在许多星球之上，留下辙痕。",
    "我要唱的歌，直到今天还没有唱出。每天我总在乐器上调理弦索。时间还没有到来，歌词也未曾填好，只有愿望的痛苦在我心中。",
    "我只在等候着爱，要最终把我交付到它手里。这是我迟误的原因，我对这延误负疚。",
    "你的负担将变成礼物，你受的苦将照亮你的路。",
    "世界上最远的距离，不是，我站在你面前，你不知道我爱你，而是，爱到痴迷，却不能说我爱你！",
    "即使爱只给你带来了哀愁，也信任它，不要把你的心关起。",
    "我们的生命似渡过一个大海，我们都相聚在这个狭小的舟中。死时，我们便到了岸，各往各的世界去了。",
    "夜的序曲是开始于夕阳西下的音乐，开始于它对难以形容的黑暗所作的庄严的赞歌。 ",
    "我们一度梦见彼此是陌生人，醒来时发现彼此是相亲相爱的。",
    "我的心是旷野的鸟，在你的眼睛里找到了它的天空。",
    "它是大地的泪点，使她的微笑保持着青春不谢。",
    "如果你因失去了太阳而流泪，那么你也失去了群星。",
    "你看不见你自己，你所看见的只是你的影子。",
    "瀑布歌唱道：“当我找到了自己的自由时，我找到了我的歌。”",
    "你微微地笑着，不同我说什么话。而我觉得，为了这个，我已等待得久了。",
    "人不能在他的历史中表现出他自己，他在历史中奋斗着露出头角。",
    "我们如海鸥之与波涛相遇似地，遇见了，走近了。海鸥飞去，波涛滚滚地流开，我们也分别了。",
    "当我们是大为谦卑的时候，便是我们最接近伟大的时候。",
]
// function set_editable_writing(editable) {
//     editable.nextElementSibling.children[0].style.display = 'block';
//     editable.nextElementSibling.children[1].style.display = 'none';
// }

// function set_editable_uploading(editable) {
//     editable.nextElementSibling.children[0].style.display = 'none';
//     editable.nextElementSibling.children[1].style.display = 'block';
// }

// function set_editable_none(editable) {
//     editable.nextElementSibling.children[0].style.display = 'none';
//     editable.nextElementSibling.children[1].style.display = 'none';
// }

function bind_listener(editor) {
    console.log(editor)
    editor.listeners.on(editor, 'click', () => {
        console.log('Button clicked!');
     }, false);

    // editor.subscribe('focus', function(event, editable) {
    //     // Do some work
    //     console.log('focus', editable);
    //     // set_editable_writing(editable);
    //     // EDITED_LOCK = true
    // });

    // editor.subscribe('editableInput', function(event, editable) {
    //     // Do some work
    //     console.log('editableInput');
    //     // EDITED_LOCK = true
    // });

    // editor.subscribe('editableBlur', function(event, editable) {
    //     // if (EDITED_LOCK == false) {
    //     //     return
    //     // }
    //     // set_editable_uploading(editable);
    //     // EDITED_LOCK = false
    //     // Do some work
    //     // update sql
    //     console.log('editableBlur', editable.parentNode)
    //     let id = editable.parentNode.dataset.id
    //     let html = editable.parentNode.childNodes[3].innerHTML.trim();
    //     let text = editable.parentNode.childNodes[3].innerText.trim();
    //     let tag = Commonexp.tag(text);
    //     // UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
    //     let sql = '{"sql":"UPDATE DONE SET HTML\= \'' + html.toHtmlEntities() + '\', CLASS\= \'' + tag.toHtmlEntities() + '\' WHERE ID\=\'' + id + '\';"}'
    //     $.post("/dcl", sql, function(result) {
    //         console.log(result);
    //         // set_editable_none(editable);
    //         // callback()
    //     });
    // });

}


/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

function addrecord(element) {
    // TODO: 这里的情况应该分为
    let target = element.parentNode.previousElementSibling
    let date = moment(target.parentNode.firstElementChild.firstElementChild.children[2].innerHTML).utc().format();
    if ($(target).hasClass('ld-harness-list-header')) {
        console.log('这日期没写过')
        let id = moment(moment()).valueOf();
        if (moment(date).format('YYYY/MM/DD') == moment().format('YYYY/MM/DD')) {
            date = getDatetime()
        }
        // let date = getDatetime();
        $.post("/dcl", '{"sql":"INSERT INTO DONE(ID,DATETIME) VALUES(\'' + id + '\',\'' + date + '\');"}', function(result) {
            console.log(result);
            htmlrecord(id, date, element);
            // callback()
        });
    } else if ($(target).hasClass('ld-harness-list-item')) {
        console.log('这日期写过，追加');
        let id = moment(moment()).valueOf();
        // let date = moment(target.parentNode.firstElementChild.firstElementChild.children[2].innerHTML).utc().format();
        if (moment(date).format('YYYY/MM/DD') == moment().format('YYYY/MM/DD')) {
            date = getDatetime()
        }
        if (target.children[1].innerText.trim() == "") {
            alert("芽衣姐，上一个还是全空啊")
            return
        }
        $.post("/dcl", '{"sql":"INSERT INTO DONE(ID,DATETIME) VALUES(\'' + id + '\',\'' + date + '\');"}', function(result) {
            console.log(result);
            htmlrecord(id, date, element);
            // callback()
        });
    } else {
        console.log('bug')
        debugger
    }

}

// TODO 两个应该合在一起
function htmlrecord(id, date, element) {
    console.log(element)
    console.log(element.parentNode)
    var target = element.parentNode
    var root = element.parentNode.parentNode
    var source = htmlToElement('<div class="ld-harness-list-item list-group-item" aria-current="true" data-id="' + id + '" data-date="' + date + '">\
        <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">\
            <small class="text-muted">' + moment(date).format('ah:mm') + '</small>\
            <small>\
            </small>\
        </div>\
        <div class="ld-harness-list-item-text">\
        </div>\
    </div>')
    root.insertBefore(source, target)

    render_editor(source.childNodes[3], {}, EDITOR_PLACEHOLDER[Math.floor(Math.random() * EDITOR_PLACEHOLDER.length)]);
    // var source_editor = new MediumEditor(source.childNodes[3], {
    //     buttonLabels: 'fontawesome',
    //     placeholder: {
    //         /* This example includes the default options for placeholder,
    //            if nothing is passed this is what it used */
    //         text: EDITOR_PLACEHOLDER[Math.floor(Math.random() * EDITOR_PLACEHOLDER.length)],
    //         hideOnClick: false
    //     }
    // });
    // bind_listener(source_editor)
}

function render_editor(element, data = {}, placeholder = "Type your message here", autofocus = false){
    var editor = new EditorJS({ 
        /** 
         * Id of Element that should contain the Editor 
         */ 
        holder: element, 

        /**
         * Previously saved data that should be rendered
         */
        data: data,
        /**
         * First Block placeholder
         */
        placeholder: placeholder,
      
        /** 
         * Available Tools list. 
         * Pass Tool's class or Settings object for each Tool you want to use 
         */ 
        tools: { 
            header: {
                class: Header, 
                inlineToolbar: ['link']
            }, 
            list: { 
                class: List, 
                inlineToolbar: true 
            },
            image: {
                class: window.ImageTool,
                config: {
                    field: 'file',
                    endpoints: {
                        byFile: 'http://localhost/file-upload', // Your backend file uploader endpoint
                        // byUrl: 'http://localhost:8008/fetchUrl', // Your endpoint that provides uploading by Url
                    },
                },
                
            },
            code: CodeTool,
            quote: Quote,
            // table: Table,
        },
        minHeight: 50,
        /**
         * If true, set caret at the first Block after Editor is ready
         */
        autofocus: autofocus,
        /**
         * onReady callback
         */
        onReady: () => {console.log('Editor.js is ready to work!')},
        /**
         * Fires when something changed in DOM
         * @param {API} api - editor.js api
         * @param event - custom event describing mutation
         */
        onChange: function(api, event){
            console.log(api, event);
            if (event.type == 'block-changed' || event.type == 'block-removed') {
                api.saver.save().then(function(OutputData){
                    let editable = api.ui.nodes.wrapper.parentNode
                    let id = editable.parentNode.dataset.id
                    let html = JSON.stringify(OutputData);
                    let text = JSON.stringify(OutputData);
                    let tag = Commonexp.tag(text);
                    // UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
                    let sql = '{"sql":"UPDATE DONE SET HTML\= \'' + html.toHtmlEntities() + '\', CLASS\= \'' + tag.toHtmlEntities() + '\' WHERE ID\=\'' + id + '\';"}'
                    $.post("/dcl", sql, function(result) {
                        console.log(result);
                        // set_editable_none(editable);
                        // callback()
                    });
                })
            }
            // for (let index = 0; index < api.blocks.getBlocksCount(); index++) {
            //     const element = api.blocks.getBlockByIndex(index+1).holder;
            //     api.listeners.on(element, 'change', () => {
            //         console.log('block changed!');
            //     }, false);
            // }
        },
    })

    // editor.save().then((outputData) => {
    //     console.log('Article data: ', outputData)
    // }).catch((error) => {
    //     console.log('Saving failed: ', error)
    // });

    // editor.isReady.then(function(data){
    //     console.log(data);
    //     editor.listeners.on(editor.block.holder, 'change', () => {
    //         console.log('block changed!');
    //     }, false);
    // })
    // bind_listener(editor)
}

document.addEventListener('keydown', function(e) {
    console.log(document.activeElement.classList)
    if(!document.activeElement.classList.contains('cdx-block')){
        return
    }
    if (e.keyCode == 83 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)) {
        e.preventDefault();
        alert('saved');
    }
});

function random(items) {
    var item = items[Math.floor(Math.random() * items.length)];
    return item
}

function html_lender_image_box(time, url) {
    let html = function() {
        /*
        <a href="/html/{0}" target="_blank">
            <img src="/html/{0}"/>
            <div class="mdui-grid-tile-actions mdui-grid-tile-actions-gradient">
                <div class="mdui-grid-tile-text">
                    <!--div class="mdui-grid-tile-title"></div-->
                    <!--div class="mdui-grid-tile-subtitle"><i class="mdui-icon material-icons">grid_on</i>Ellie Goulding</div-->
                    <div class="mdui-grid-tile-text"><div class="mdui-grid-tile-title">{1}</div></div>
                </div>
                <!--div class="mdui-grid-tile-buttons">
                    <a class="mdui-btn mdui-btn-icon"><i class="mdui-icon material-icons">star_border</i></a>
                </div-->
            </div>
        </a>
        */
    }
    return '<div class="mdui-grid-tile">' + html.getMultiLine().format(url, moment(time).format('Y-MM-DD')) + '</div>'
}

function html_badges(badges) {
    console.log(badges)
    var items = ['badge bg-primary', 'badge bg-secondary', 'badge bg-success', 'badge bg-danger', 'badge bg-warning text-dark', 'badge bg-info text-dark', 'badge bg-light text-dark', 'badge bg-dark'];
    let badge = ''
    String.fromHtmlEntities(badges).split(",").forEach(function(t) {
        badge += '<span class="' + random(items) + '">' + t + '</span>\n'
    })
    return badge
}

function html_lender_list_box(time, obj, id) {
    let header = '\
    <li class="ld-harness-list-header list-group-item list-group-item-secondary mdui-color-theme-50">\
        <div class="row">\
            <div class="col-md-2">' + moment(time).format("dddd") + '</div>\
            <div class="col-md-8"></div>\
            <div class="col-md-2">' + time + '</div>\
        </div>\
    </li>'

    let items = ''
    for (let index = 0; index < obj.length; index++) {
        const element = obj[index];
        let badge = html_badges(element[4])

        let html = function() {
            /*
            <div href="#" class="ld-harness-list-item list-group-item" aria-current="true" data-id="{0}" data-date="{1}">
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <div class="text-muted" style="margin: auto 0;">
                        <small>{2}</small>
                    </div>
                    <div>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="clipCard(this)" mdui-tooltip="{content: '复制', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard-check" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                            </svg></button>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="deleteCard(this)" mdui-tooltip="{content: '删除', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg></button>
                            
                    </div>
                </div>
                <div class="ld-harness-list-item-text"></div>
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <small class="writing text-muted">Writing
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                            <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"/>
                            </svg></small>
                    <small class="uploading text-muted">Uploading
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-upload" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
                            <path fill-rule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3z"/>
                            </svg></small>
                    <small>{3}</small>
                </div>
            </div>
            */
        };

        // items += html.getMultiLine().format(moment(element[1]).format('LT'), badge, element[2]);
        items += html.getMultiLine().format(element[0], moment(element[1]), moment(element[1]).format('ah:mm'), badge);
    }

    let add = '\
    <div class="ld-harness-list-add list-group-item" aria-current="true">\
        <div class=" d-grid gap-2 col-6 mx-auto" onclick="addrecord(this)">\
            <button type="button" class="btn btn-outline-light"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">\
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>\
            </svg></button>\
        </div>\
    </div>'

    return '<div id="'+ id +'" class="list-group">' + header + items + add + '</div>'
}

// 输出UTC
// 按中国时区的UTC时间，所以输出的应该是一个八点到八点的时间
function getWeekRangeUTC(offset = 0) {
    let weekOfday = moment().format('E'); //计算今天是这周第几天
    let monday = moment(moment().format('YYYY-MM-DD')).subtract(weekOfday - 1, 'days');
    monday = monday.add(offset, 'weeks');
    let sunday = moment(monday).add(7, 'days');
    return [monday.utc().format(), sunday.utc().format()]
}

// offset: 0, current week
// offset: -1, last week
function getWeekdate(offset = 0, sort = 'asc', format = 'YYYY/MM/DD') {
    console.log(offset, format)
    let weekOfday = moment().format('E'); //计算今天是这周第几天
    let monday = moment().subtract(weekOfday, 'days');
    monday = monday.add(offset, 'weeks');
    let dates = []
    if (sort == 'asc') {
        for (let index = 1; index < 8; index++) {
            const element = index;
            let someday = moment(monday).add(index, 'days');
            if (someday <= moment()) {
                dates.push(someday.format(format))
            }
        }
    } else if (sort == 'desc') {
        for (let index = 7; index > 0; index--) {
            const element = index;
            let someday = moment(monday).add(index, 'days');
            if (someday <= moment()) {
                dates.push(someday.format(format))
            }
        }
    } else {

    }

    return dates
}
// 按日期重新组织数据
// 这里应该按日期，有的往里加，而不是简单构建map
// 输入UTC
// 输出locale
function list2daily(list) {
    let result = {};
    let weekdates = getWeekdate(CURRENT_WEEK, 'desc');
    for (let index = 0; index < weekdates.length; index++) {
        const element = weekdates[index];
        result[element] = []
    }

    console.log(list);
    for (let index = 0; index < list.length; index++) {
        const element = list[index];
        let day = locDatetime(element[1], 'L')
        if (day in result) {
            result[day].push(element)
        }
    }
    return result
}

// 输入UTC
// 输出locale
function list2dailyImage(list) {
    let week = {};
    let weekdates = getWeekdate(CURRENT_WEEK, 'desc');
    for (let index = 0; index < weekdates.length; index++) {
        const element = weekdates[index];
        week[element] = []
    }

    console.log(list);
    let results = []
    for (let index = 0; index < list.length; index++) {
        const element = list[index];
        let day = locDatetime(element.created_time * 1000, 'L');
        if (day in week) {
            results.push(element);
        }
    }
    return results
}

function lender_list_init() {
    let weekdate = getWeekRangeUTC(CURRENT_WEEK);
    // 传入between的只能是单引号
    // 分号不要忘记了
    // $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE DATETIME BETWEEN \'2020-06-12\' AND \'2022-06-18\'; "}', function(result) {
    $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE DATETIME between \'' + weekdate[0] + '\' and \'' + weekdate[1] + '\'; "}', function(result) {
        var data = JSON.parse(result)
        data = list2daily(data)
        console.log(data)
        $(".ld-harness").empty()
        for (const key in data) {
            if (Object.hasOwnProperty.call(data, key)) {
                const element = data[key];
                console.log(element)
                let id  = moment(key).format('x')
                let ele = createNode(html_lender_list_box(key, element, id))
                $(".ld-harness").append(ele);
                harness_editable(ele, '//*[@id="'+id+'"]//*[@class="ld-harness-list-item-text"]', element)
                // let item = document.evaluate('//*[@class="ld-harness-list-item-text"]', ele, null, XPathResult.ANY_TYPE, null);
                // for (let index = 0; index < element.length; index++) {
                //     let dom = item.iterateNext();
                //     console.log(dom)
                //     render_editor(dom, JSON.parse(String.fromHtmlEntities(element[index][2])), EDITOR_PLACEHOLDER[Math.floor(Math.random() * EDITOR_PLACEHOLDER.length)])
                // }
            }
        }
    });
}

function lender_image_init(callback) {
    $.get("/userdata", function(result) {
        var data = JSON.parse(result)
        data = list2dailyImage(data)
        console.log(data)
        $(".ld-images").empty();

        for (let index = 0; index < data.length; index++) {
            const element = data[index];
            console.log(element);
            $(".ld-images").append(html_lender_image_box(element.created_time * 1000, element.url));
        }

        if (typeof callback === "function") {
            callback()
        }
    });
}

function initDatetime() {
    moment.locale('zh-cn');
}

function getDatetime() {
    return moment.utc().format();
}

function locDatetime(utcstring, type = 'LLLL') {
    return moment(utcstring).format(type); // 2022年5月3日星期二下午5点17分

    // moment.locale();         // zh-cn
    // moment().format('LT');   // 17:19
    // moment().format('LTS');  // 17:19:50
    // moment().format('L');    // 2022/05/03
    // moment().format('l');    // 2022/5/3
    // moment().format('LL');   // 2022年5月3日
    // moment().format('ll');   // 2022年5月3日
    // moment().format('LLL');  // 2022年5月3日下午5点19分
    // moment().format('lll');  // 2022年5月3日 17:19
    // moment().format('LLLL'); // 2022年5月3日星期二下午5点19分
    // moment().format('llll'); // 2022年5月3日星期二 17:19
}

function harness_editable(ele, xpath, element, autofocus=false) {
    let item = document.evaluate(xpath, ele, null, XPathResult.ANY_TYPE, null);
    for (let index = 0; index < element.length; index++) {
        let dom = item.iterateNext();
        console.log(dom)
        render_editor(dom, JSON.parse(String.fromHtmlEntities(element[index][2])), EDITOR_PLACEHOLDER[Math.floor(Math.random() * EDITOR_PLACEHOLDER.length)], autofocus)
    }
    
    // bind_listener(editor)
    // (Firefox 插入<br>、IE/Opera将使用<p>、 Chrome/Safari 将使用 <div>）
    // var editor = new MediumEditor('.ld-harness-list-item-text', {
    //     buttonLabels: 'fontawesome',
    //     placeholder: {
    //         /* This example includes the default options for placeholder,
    //            if nothing is passed this is what it used */
    //         text: EDITOR_PLACEHOLDER[Math.floor(Math.random() * EDITOR_PLACEHOLDER.length)],
    //         hideOnClick: false
    //     }
    // });
    // bind_listener(editor)
}

function clipCard(aux) {
    let targets = aux.parentNode.parentNode.nextElementSibling.children;
    let textContent = ''
    for (const iterator of targets) {
        textContent += iterator.textContent + "\n"
    }
    // navigator.clipboard.writeText(target.textContent).then(function() {
    //     /* clipboard successfully set */
    // }, function() {
    //     /* clipboard write failed */
    // });
    // return
    let tmpele = document.createElement("textarea"); //创建input节点
    aux.appendChild(tmpele); //将节点添加到body
    tmpele.value = textContent; //将需要复制的字符串赋值到input的value中
    tmpele.select(); //选中文本(关键一步)
    document.execCommand("copy"); //执行浏览器复制功能(关键一步)
    aux.removeChild(tmpele); //复制完成后删除节点

    // console.log(target.textContent);
    // target.setAttribute("value", target.textContent);
    // target.select();
    // document.execCommand('copy', false, target.textContent);

    // let that = this
    // let txa = document.createElement('textarea')
    // let txval = 'SN:' + that.sn1 + '\n' + 'MAC:' + that.mac1 + '\n' + 'IMEI:' + that.imei1 + '\n' + 'PORT:' + that.port1;
    // // console.log('copy val:', txval)
    // txa.value = txval
    // document.body.appendChild(txa)
    // txa.select()
    // let res = document.execCommand('copy')
    // document.body.removeChild(txa)
    // console.log('copy success')
}

function deleteCard(aux) {
    console.log()
    let card = aux.parentNode.parentNode.parentNode
    let cardid = card.dataset.id;
    let sql = '{"sql":"UPDATE DONE SET STATUS\= \'1\' WHERE ID\=\'' + cardid + '\';"}'
    let timer_is_on = 0;

    card.style.display = 'none';
    mdui.snackbar({
        message: '[Lender] Deleting',
        buttonText: 'undo',
        onClick: function() {
            // mdui.alert('点击了 Sanckbar');
        },
        onButtonClick: function() {
            // mdui.alert('点击了按钮');
            timer_is_on = 1;
        },
        onClose: function() {
            // mdui.alert('关闭了');
            if (timer_is_on == 0) {
                $.post("/dcl", sql, function(result) {
                    console.log(result);
                    card.remove();
                });
            } else {
                card.style.display = 'block';
            }
        }
    });

}


function prevWeek() {
    InitWeek(-1)
    CURRENT_WEEK -= 1
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
}

function nextWeek() {
    CURRENT_WEEK += 1
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
}

function thisWeek() {
    CURRENT_WEEK = 0
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
    lender_image_init(null);
}

function InitWeek(week_offset = 0) {
    if (week_offset == 0) {
        CURRENT_WEEK = 0;
    }
    CURRENT_WEEK += week_offset
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
    lender_image_init(null);
}

var toastTrigger = document.getElementById('liveToastBtn')
var toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
    toastTrigger.addEventListener('click', function() {
        var toast = new bootstrap.Toast(toastLiveExample)

        toast.show()
    })
}

initDatetime();
InitWeek(0);


function html_search_list_box(time, obj, id) {
    let header = '\
    <li class="ld-harness-list-header list-group-item list-group-item-secondary mdui-color-theme-50">\
        <div class="row">\
            <div class="col-md-2">' + moment(time).format("dddd") + '</div>\
            <div class="col-md-8"></div>\
            <div class="col-md-2">' + time + '</div>\
        </div>\
    </li>'

    let items = ''
    for (let index = 0; index < obj.length; index++) {
        const element = obj[index];
        let badge = html_badges(element[4])

        let html = function() {
            /*
            <div href="#" class="ld-harness-list-item list-group-item" aria-current="true" data-id="{0}" data-date="{1}">
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <div class="text-muted" style="margin: auto 0;">
                        <small>{2}</small>
                    </div>
                    <div>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="clipCard(this)" mdui-tooltip="{content: '复制', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard-check" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                            </svg></button>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="deleteCard(this)" mdui-tooltip="{content: '删除', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg></button>
                            
                    </div>
                </div>
                <div class="ld-harness-list-item-text"></div>
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <small class="writing text-muted">Writing
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                            <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"/>
                            </svg></small>
                    <small class="uploading text-muted">Uploading
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-upload" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
                            <path fill-rule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3z"/>
                            </svg></small>
                    <small>{4}</small>
                </div>
            </div>
            */
        };

        // items += html.getMultiLine().format(moment(element[1]).format('LT'), badge, element[2]);
        items += html.getMultiLine().format(element[0], moment(element[1]), locDatetime(element[1], 'L') + " " + moment(element[1]).format('ah:mm'), String.fromHtmlEntities(element[2]), badge);
    }

    let add = '\
    <div class="ld-harness-list-add list-group-item" aria-current="true">\
        <div class=" d-grid gap-2 col-6 mx-auto" onclick="addrecord(this)">\
            <button type="button" class="btn btn-outline-light"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">\
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>\
            </svg></button>\
        </div>\
    </div>'

    return '<div id="'+id+'" class="list-group">' + items + '</div>'
}

function search_run(obj){
    inp = obj.previousElementSibling;
    console.log(inp.value)
    if (inp.value == "") {
        return
    }
    console.log(inp.value.toHtmlEntities())
    $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE CLASS like \'%' + inp.value.toHtmlEntities() + '%\' or HTML like \'%' + inp.value.toHtmlEntities() + '%\'; "}', function(result) {
        var datas = JSON.parse(result)
        console.log(datas)
        // data = list2daily(data)
        $("#search-result").empty()
        let key = 1
        // $("#search-result").append(html_search_list_box(key, datas));
        // harness_editable()
        let id  = moment(key).format('x')
        let ele = createNode(html_search_list_box(key, datas, id))
        $("#search-result").append(ele);
        harness_editable(ele, '//*[@id="'+id+'"]//*[@class="ld-harness-list-item-text"]', datas, false)
        $("#search-result").show()
});
}

function search_close(obj){
    console.log(obj)
    $("#search-result").hide()
    // $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE tag like \'%' + html.toHtmlEntities() + '%\' or text \'' + html.toHtmlEntities() + '\'; "}', function(result) {
    //     var data = JSON.parse(result)
    //     data = list2daily(data)
    //     console.log(data)
    //     $("#search-result").empty()
    //     for (const key in data) {
    //         if (Object.hasOwnProperty.call(data, key)) {
    //             const element = data[key];
    //             console.log(element)
    //             $("#search-result").append(html_lender_list_box(key, element));
    //         }
    //     }
    //     callback()
    // });
}
// $(function() {
//     document.getElementById("changetheme").onchange = function (obj) {
//         console.log(obj.text)
//         document.body.classList = ['mdui-theme-primary-' + theme]
//     };
// });

function changetheme(theme) {
    console.log(theme)
    document.body.classList = ['mdui-theme-primary-' + theme]
}
// $(window).load(function() {});

function getDateDura(date) {
    let m2 = moment(); //当下时间
    // let m2=moment('2019-12-18 10:10:00');
    let m1 = moment(date);
    let du = moment.duration(m2 - m1, 'ms'); //做差
    let days = du.get('days');
    let hours = du.get('hours');
    let mins = du.get('minutes');
    let ss = du.get('seconds');
    console.log(days, hours, mins, ss);
    //  输出结果为   01天08时09分40秒
    if (days > 0) {
        date = moment(date).format("YYYY年MM月DD日");
        return date
    } else if (hours > 0) {
        return hours + '小时之前'
    } else {
        return mins + '分钟之前'
    }
}


// const editor = new EditorJS({ 
//     /** 
//      * Id of Element that should contain the Editor 
//      */ 
//     holder: 'editorjs', 
  
//     /** 
//      * Available Tools list. 
//      * Pass Tool's class or Settings object for each Tool you want to use 
//      */ 
//     tools: { 
//         header: {
//             class: Header, 
//             inlineToolbar: ['link'] 
//         }, 
//         list: { 
//             class: List, 
//             inlineToolbar: true 
//         } 
//     },
//     /**
//     * onReady callback
//     */
//     onReady: () => {
//         console.log('Editor.js is ready to work!')
//     },
//     /**
//      * Previously saved data that should be rendered
//      */
//     data: {
//         "time": 1550476186479,
//         "blocks": [
//            {
//               "id": "oUq2g_tl8y",
//               "type": "header",
//               "data": {
//                  "text": "Editor.js",
//                  "level": 2
//               }
//            },
//            {
//               "id": "zbGZFPM-iI",
//               "type": "paragraph",
//               "data": {
//                  "text": "Hey. Meet the new Editor. On this page you can see it in action — try to edit this text. Source code of the page contains the example of connection and configuration."
//               }
//            },
//            {
//               "id": "qYIGsjS5rt",
//               "type": "header",
//               "data": {
//                  "text": "Key features",
//                  "level": 3
//               }
//            },
//            {
//               "id": "XV87kJS_H1",
//               "type": "list",
//               "data": {
//                  "style": "unordered",
//                  "items": [
//                     "It is a block-styled editor",
//                     "It returns clean data output in JSON",
//                     "Designed to be extendable and pluggable with a simple API"
//                  ]
//               }
//            },
//            {
//               "id": "AOulAjL8XM",
//               "type": "header",
//               "data": {
//                  "text": "What does it mean «block-styled editor»",
//                  "level": 3
//               }
//            },
//            {
//               "id": "cyZjplMOZ0",
//               "type": "paragraph",
//               "data": {
//                  "text": "Workspace in classic editors is made of a single contenteditable element, used to create different HTML markups. Editor.js <mark class=\"cdx-marker\">workspace consists of separate Blocks: paragraphs, headings, images, lists, quotes, etc</mark>. Each of them is an independent contenteditable element (or more complex structure) provided by Plugin and united by Editor's Core."
//               }
//            }
//         ],
//         "version": "2.8.1"
//      },
//     /**
//     * onChange callback
//     */
//     onChange: (api, event) => {
//         console.log('Now I know that Editor\'s content changed!', event)
//     },
//     /**
//      * This Tool will be used as default 
//      */
//     defaultBlock: 'myOwnParagraph',

//     placeholder: 'Let`s write an awesome story!'
// })


function createNode(htmlStr) {
    var div = document.createElement("div");
    div.innerHTML = htmlStr;
    return div.childNodes[0];
}