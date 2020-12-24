var qFields = new Map();
qFields.set(1, new Set([1, 2]));

function findLeastNum(map) {
    for (let i = 1; i < map.size+2; i++) {if (!map.has(i)) return i;}
}

function findNextNum(numsSet, num) {
    var bigNums = Array.from(numsSet).filter(n => n > num);
    return Math.min.apply(null, bigNums);
}

function addQuestionField() {
    const qNum = findLeastNum(qFields);
    qFields.set(qNum, new Set([1]));
    const divElement = document.createElement("div");
    let path = document.getElementById("vip-icon").src;
    divElement.innerHTML = `
        <div>
            <img style="width: 4%" src="${path}">
            <label class="text-second-org" for="id_question${qNum}">Вопрос #${qNum}</label>
            <input type="text" name="question${qNum}" required id="id_question${qNum}">
            <a id="q_delete${qNum}" class="text-second-org icon std-link" style="text-align: left; display: inline-block" onclick="return deleteField(this, ${qNum})" href="#">X</a>
            <br id="br${qNum}">
            <label for="id_question${qNum}_type">Тип вопроса #${qNum}:</label>
            <select name="question${qNum}_type" class="std-select text-second-org" required id="id_question${qNum}_type">
                <option value="st">Small text</option>
                <option value="bt">Big text</option>
                <option value="r">Radio</option>
                <option value="c">Checkbox</option>
            </select>
        </div>
        <ul id="answers${qNum}" style="list-style: none">
            <div id="answer${qNum}_1" class="text-second poll-field-wrapper">
                <li>
                    <label for="id_answer${qNum}_1">Answer #1:</label>
                    <input type="text" name="answer${qNum}_1" required id="id_answer${qNum}_1">
                </li>
            </div>
            <a href="#" class="text-second-org icon std-link" style="text-align: left" id="add_answer_ref${qNum}" onclick="return addPossibleAnswer(${qNum})">[+]</a>
        </ul>`;
    divElement.id = "question"+qNum;
    divElement.classList.add("poll-field-wrapper");
    divElement.classList.add("margin-class");
    const lastChild = document.getElementById("add_field_ref");
    if (qNum > 2) document.getElementById("q_delete"+(qNum-1)).remove();
    document.getElementById("questions").insertBefore(divElement, lastChild);
    return false;
}

function deleteField(field, qNum) {
    if (qNum === 1)
        return false;
    let parent = field.parentNode.parentNode.parentNode;
    parent.removeChild(field.parentNode.parentNode);
    qFields.delete(qNum);
    if (qNum !== 2){
        let divElement = document.createElement("a");
        divElement.setAttribute("href", "#");
        let onclickValue = `return deleteField(this, ${qNum-1})`;
        divElement.setAttribute("onclick", onclickValue);
        divElement.id = "q_delete"+(qNum-1);
        divElement.text = "X";
        divElement.classList.add("text-second-org");
        divElement.classList.add("std-link");
        divElement.style.display = "inline-block";
        let br = document.getElementById("br"+(qNum-1));
        br.parentNode.insertBefore(divElement, br);
    }
    return false;
}

function deletePossibleAnswer(field, qNum, aNum) {
    if (aNum === 1)
        return false;
    let contDiv = field.parentNode;
    contDiv.parentNode.removeChild(contDiv);
    let answers = qFields.get(qNum);
    answers.delete(aNum);
    qFields.set(qNum, answers);
    if (aNum !== 2) {
        let lastChild = document.getElementById("id_answer" + qNum + "_" + (aNum - 1));
        let deleteBtn = document.createElement("a");
        deleteBtn.setAttribute("href", "#");
        let onclickValue = `return deletePossibleAnswer(this, ${qNum}, ${aNum - 1})`;
        deleteBtn.setAttribute("onclick", onclickValue);
        deleteBtn.id = "delete" + qNum;
        deleteBtn.text = "X";
        deleteBtn.classList.add("text-second");
        deleteBtn.style.display = "inline-block";
        lastChild.parentNode.appendChild(deleteBtn);
    }
    return false;
}

function addPossibleAnswer(qNum) {
    let answers = qFields.get(qNum);
    const aNum = Math.max.apply(null, Array.from(answers))+1;
    answers.add(aNum);
    qFields.set(qNum, answers);
    let divElement = document.createElement("div");
    divElement.innerHTML = `
        <li>
            <label for="id_answer${qNum}_${aNum}">Answer #${aNum}:</label>
            <input type="text" name="answer${qNum}_${aNum}" required id="id_answer${qNum}_${aNum}">
            <a style="display: inline-block" class="text-second" onclick="return deletePossibleAnswer(this, ${qNum}, ${aNum})" id="delete${qNum}" href="#">X</a>
        </li>`;
    divElement.id = "answer"+qNum+"_"+aNum;
    divElement.classList.add("text-second");
    divElement.classList.add("poll-field-wrapper");
    if (aNum !== 2) document.getElementById("delete"+qNum).remove();
    let lastChild = document.getElementById("add_answer_ref"+qNum);
    document.getElementById("answers"+qNum).insertBefore(divElement, lastChild);
    return false;
}

// $('.select').each(function() {
//     const _this = $(this),
//         selectOption = _this.find('option'),
//         selectOptionLength = selectOption.length,
//         selectedOption = selectOption.filter(':selected'),
//         duration = 450; // длительность анимации 
//
//     _this.hide();
//     _this.wrap('<div class="select"></div>');
//     $('<div>', {
//         class: 'new-select',
//         text: _this.children('option:disabled').text()
//     }).insertAfter(_this);
//
//     const selectHead = _this.next('.new-select');
//     $('<div>', {
//         class: 'new-select__list'
//     }).insertAfter(selectHead);
//
//     const selectList = selectHead.next('.new-select__list');
//     for (let i = 1; i < selectOptionLength; i++) {
//         $('<div>', {
//             class: 'new-select__item',
//             html: $('<span>', {
//                 text: selectOption.eq(i).text()
//             })
//         })
//             .attr('data-value', selectOption.eq(i).val())
//             .appendTo(selectList);
//     }
//
//     const selectItem = selectList.find('.new-select__item');
//     selectList.slideUp(0);
//     selectHead.on('click', function() {
//         if ( !$(this).hasClass('on') ) {
//             $(this).addClass('on');
//             selectList.slideDown(duration);
//
//             selectItem.on('click', function() {
//                 let chooseItem = $(this).data('value');
//
//                 $('select').val(chooseItem).attr('selected', 'selected');
//                 selectHead.text( $(this).find('span').text() );
//
//                 selectList.slideUp(duration);
//                 selectHead.removeClass('on');
//             });
//
//         } else {
//             $(this).removeClass('on');
//             selectList.slideUp(duration);
//         }
//     });
// });