var template = "<span id=\"{0}\" class=\"label {1} _tag\" >{2}&nbsp<a href=\"#\" data-toggle=\"tooltip\" title=\"删除条件\" class=\"close-tag\" onclick=\"closeIt('{3}', '{4}')\">&times</a></span>"
/*global map*/
var tagsMap = new Map()

$(document).ready(function () {
    $("#searchForm").on("submit", function () {
        search($(this));
        return false;
    });
    $("#searchForm input").click(function() {
        search($(this))
    })

});
_setEvent("companyId",  "comp_{0}", template, "label-warning")
_setEvent("tagId", "tags_{0}", template, "label-info")
_setEvent("clauseName", "clause_{0}", template, "label-danger")


function _setEvent(name, keyPlate, template, css) {
    var ckBox = $("[name="+name+"][type=checkbox]")
    var radio = $("[name="+name+"][type=radio]")
    radio.click(function () {
        ckBox.each(function (i, elem) {
            var cb = $(elem)
            if (cb.attr('checked') === 'checked' || cb.attr('checked') === true){
                tagsMap.remove(keyPlate.format(cb.val()))
                cb.removeAttr('checked')
            }
        })
        print_tags(tagsMap)
        search($("#searchForm"))
    })

    /**设置复选框事件*/
    ckBox.each(function (i, elem) {
        var cb = $(elem)
        cb.click(function () {
            var key = keyPlate.format(cb.val())
            var label = template.format(cb.val(), css, cb.parent().text(), name, cb.val())
            if (cb.attr('checked') === 'checked' || cb.attr('checked') === true) {
                if ($("[name="+name+"][type=checkbox]:checked").length === 0) {
                    radio.click()
                    radio.attr("checked", 'true')
                }
                tagsMap.remove(key)
                cb.removeAttr('checked')
            } else {
                cb.attr('checked', 'true')
                radio.removeAttr("checked")
                tagsMap.put(key, label)
            }
            print_tags(tagsMap)
            search($("#searchForm"))
        })
    })
}

function closeIt(name, value) {
    $("[name="+name+"][type=checkbox][value="+value+"]").click()
}

function print_tags(map) {
    var conditions = $("#conditions")
    conditions.empty()
    var p = conditions.append("<p></p>").last()
    map.each(function (key, value, index) {
        if ((index + 1) % 8 === 0) {
            p = conditions.append("<p></p>").last()
        }
        p.append(value)
    })
}


function search(form) {
    var message = form.serializeArray()
    $.postJSON("/", message, function (response) {
        $("#result").empty().append(response)
    });
}
/**
 * string format:
 * useage:
 * "<a href=\"{0}\">{1}</>".format('http://www.', 'link to')
 * "<a href=\"{url}\">{name}</>".format({url:'http://www.', name:'link to'})
 * */
String.prototype.format = function (args) {
    if (arguments.length > 0) {
        var result = this
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                var reg = new RegExp("({" + key + "})", "g")
                result = result.replace(reg, args[key])
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] == undefined) {
                    return ""
                }
                else {
                    var reg = new RegExp("({[" + i + "]})", "g")
                    result = result.replace(reg, arguments[i])
                }
            }
        }
        return result
    }
    else {
        return this
    }
}


/**
 * 自定义key-value Map
 * 支持添加，删除，获取，迭代，keys等基本操作
 * @constructor
 */
function Map() {
    this.keys = new Array()
    this.data = new Object()

    this.put = function (key, value) {
        if (this.data[key] == null) {
            this.keys.push(key)
        }
        this.data[key] = value
    }

    this.get = function (key) {
        return this.data[key]
    }

    this.remove = function (key) {
        this.keys.remove(key)
        this.data[key] = null
    }

    this.each = function (fn) {
        if (typeof fn != 'function') {
            return
        }
        var len = this.keys.length
        for (var i = 0; i < len; i++) {
            var k = this.keys[i]
            fn(k, this.data[k], i)
        }
    }

    this.entrys = function () {
        var len = this.keys.length
        var entrys = new Array(len)
        for (var i = 0; i < len; i++) {
            entrys[i] = {
                key: this.keys[i],
                value: this.data[i]
            }
        }
        return entrys
    }

    this.isEmpty = function () {
        return this.keys.length == 0
    }

    this.size = function () {
        return this.keys.length
    }
}
/**
 * array remove method
 * @returns {*}
 */
Array.prototype.remove = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

/**
 * parse a int number to readable date
 * @param year
 * @returns {string}
 * Usage: to_date_str(400)--> return 1年1个月5天
 */
function to_date_str(year) {
    try {
        parseInt(year)
    } catch(err) {
        alert("Error on parse "+year+" to Int")
        return "0"
    }
    if (year < 365 ) {
        if (year < 30) {
            return year + "天"
        }
        if (year % 30 == 0){
            return year / 30 + "个月"
        } else {
             return parseInt(year / 30) + "个月" + year % 30 + "天"
        }
    } else {
        if (year % 365 == 0) {
            return (year / 365) + "年"
        } else {
            return parseInt(year / 365) + "年" + to_date_str((year % 365))
        }
    }
}

jQuery.postJSON = function(url, args, callback) {
//    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
            if (callback) callback(response)
    }, error: function(response) {
        console.log("ERROR:", response)
    }});
};

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};