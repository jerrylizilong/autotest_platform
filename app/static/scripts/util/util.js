    //检查下拉框选中id
function get_multiple_select_value(objSelectId){
    var objSelect = document.getElementById(objSelectId);
    var length = objSelect.options.length;
    var value = '';
    for(var i=0;i<length;i++){
        if(objSelect.options[i].selected==true){
        if(value==''){
        value = objSelect.options[i].value;
        }else{
        value = value+','+objSelect.options[i].value;}

        }
    }
    return value;
}

function selectOnchang(obj){
//获取被选中的option标签选项
var value = obj.options[obj.selectedIndex].value;
//alert(value);
}


 function removeOptions(selectObj)
 {
 if (typeof selectObj != 'object')
 {
 selectObj = document.getElementById(selectObj);
 }
 // 原有选项计数
 var len = selectObj.options.length;
 for (var i=0; i < len; i++) {
 // 移除当前选项
 selectObj.options[0] = null;
 }
 }
 /*
 * @param {String || Object]} selectObj 目标下拉选框的名称或对象，必须
 * @param {Array} optionList 选项值设置 格式：[{txt:'北京', val:'010'}, {txt:'上海', val:'020'}] ，必须
 * @param {String} firstOption 第一个选项值，如：“请选择”，可选，值为空
 * @param {String} selected 默认选中值，可选
 */
 function setSelectOption(selectObj, optionList, firstOption, selected) {
 if (typeof selectObj != 'object')
 {
 selectObj = document.getElementById(selectObj);
 }
 // 清空选项
 removeOptions(selectObj);
 // 选项计数
 var start = 0;
 // 如果需要添加第一个选项
 if (firstOption) {
 selectObj.options[0] = new Option(firstOption, '');
 // 选项计数从 1 开始
 start ++;
 }
// alert();
 var len = optionList.length;
 for (var i=0; i < len; i++) {
 // 设置 option
 selectObj.options[start] = new Option(optionList[i].txt, optionList[i].val);
 // 选中项
 if(selected == optionList[i].val)  {
 selectObj.options[start].selected = true;
 }
 // 计数加 1
 start ++;
 }
 }

var moduleArr = [];
moduleArr['公共用例'] =
[
 {txt:'public', val:'public'}
 ];
moduleArr['普通用例'] =
[
 {txt:'模块1', val:'模块1'},
 {txt:'模块2', val:'模块2'},
 {txt:'模块3', val:'模块3'}
 ];
function setModule(type)
{
 setSelectOption('module', moduleArr[type], '-请选择-');
}



function setIframeHeight(iframe) {
if (iframe) {
var iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
if (iframeWin.document.body) {
iframe.height = iframeWin.document.documentElement.scrollHeight || iframeWin.document.body.scrollHeight;
}
}
};

window.onload = function () {
setIframeHeight(document.getElementById('external-frame'));
};