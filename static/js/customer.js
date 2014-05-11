//设置下拉框的事件
setEvents("#min_age_list", "a", function () {
    $("#minAge").val(this.text)
})

setEvents("#max_age_list", "a", function () {
    $("#maxAge").val(this.text)
})


function setEvents(id, find, func) {
    $(id).find(find).each(function (i, elem) {
        $(elem).click(func)
    })
}

function generate() {
    var oldval = $("#clause_limit").val()
    var clause = $("#clause").val()
    var limit = $("#limits").val()
    if (clause != "" && limit != "") {
        var value = clause + ":" + limit
        if (oldval != "") {
            value = oldval + ", " + value
        }
        $("#clause_limit").val(value)
        limit = $("#limits").val("")
        $("#clause_limit").css("display", "inline")
    }
}

$(document).ready(function () {
     $.validator.addMethod("isRegularAge", function(val, element, param){
         var num = date_to_num(val)
         if (num > 0 ) {
             $(element).val(date_to_num(val))
             return true
         }
         return false
     }, "Not Regular Age")
     $.validator.addMethod("greaterThan", function(val, element, param){
        return val > $(param).val()
     }, "Max age should greater than min age")
     $('#insu-form').validate(
         {
//             debug: true,
             rules: {
                 proName: {
                     minlength: 2,
                     required: true
                 },
                 minAge: {
                     isRegularAge: true,
                     min: 1,
                     max: 36500,
                     required: true
                 },
                 maxAge: {
                     isRegularAge:true,
                     required: true,
                     greaterThan: minAge
                 },
                 companyId: {
                     required: true
                 },
                 categoryId: {
                     required: true
                 },
                 description: {
                     required:true
                 },
                 notice:{
                     required: true
                 },
                 example:{
                     required: true
                 },
                 suitable:{
                     required: true
                 },
                 price:{
                     min:0,
                     number:true,
                     required: true
                 },
                 salesVolume:{
                     required: true,
                     min:1
                 },
                 buyCount:{
                     required: true,
                     min:0
                 }
                
             },
             highlight: function (element) {
                 $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
             },
             success: function (element) {
                 element.text('OK!').addClass('valid')
                        .closest('.form-group').removeClass('has-error').addClass('has-success');

             }
         });
}); //

/**
 *转换时间字符到整数
 * @param age
 * @returns {number}
 * Usage:
 * date_to_num("2年") rt:730
 * date_to_num("2岁") rt:730
 * date_to_num("3天") rt:3
 */
function date_to_num(arg) {

    if (isRegularNum(arg)) {
        return arg
    }
    arg = arg.replace("岁", "年")
    var idx_y = arg.indexOf("年")
    var idx_d = arg.indexOf("天")
    if (idx_y > -1 && idx_y == arg.length-1) {
        var num = arg.slice(0, idx_y)
        if (isRegularNum(num)) {
            if (parseInt(num) > 100){
                return -1
            }
            return parseInt(num) * 365
        }
        return -1
    }
    if (idx_d > -1 && idx_d == arg.length-1) {
        var num = arg.slice(0, idx_d)
        if (isRegularNum(num)) {
            return parseInt(num)
        }
        return -1
    }
    return -1
}
/**
 * 转换价格字符到整数
 * @param str
 * @returns {number}
 * usage str_to_name("5百")
 * usage str_to_name("5千")
 * usage str_to_name("10万")
 * usage str_to_name("10０万")
 */
function str_to_num(str){
    if (isRegularNum(str)) {
        return str
    }
    if (str.indexOf("百") > -1) {
        var num = str.slice(0, str.indexOf("百"))
        if (isRegularNum(num)) {
            return parseInt(num) * 100.0
        }
    }
    if (str.indexOf("千") > -1) {
        var num = str.slice(0, str.indexOf("千"))
        if (isRegularNum(num)) {
            return parseInt(num) * 1000.0
        }
    }
    if (str.indexOf("万") > -1) {
        var num = str.slice(0, str.indexOf("万"))
        if (isRegularNum(num)) {
            return parseInt(num) * 10000.0
        }
    }
    return -1
}

function isRegularNum(num) {
    var reg = new RegExp("^[0-9]*$");
    if (reg.test(num) && parseInt(num) > 0) {
        return true
    }
    return false
}
function isImage(name) {
//    var reg = new RegExp("/(\\.|\/)(gif|jpe?g|png)$/i");
    if (/(\.|\/)(gif|jpe?g|png)$/i.test(name)) {
        return true
    }
    return false
}