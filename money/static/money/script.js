// Кнопки удаления Типов, Статусов, Категорий и Субкатегорий
const deleteItem = document.querySelectorAll(".delete-item");

deleteItem.forEach((btn)=>{
    btn.addEventListener("click", () => {
        const itemType = btn.dataset.formType;
        const itemId = btn.dataset.pk; 

        fetch("delete_item/", {
            method: "POST",
   
            body: JSON.stringify({
                item_type: itemType,
                item_id: itemId,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                // например, перезагружаем страницу или удаляем элемент из DOM
                location.reload();
            } else {
                alert("Ошибка: " + data.error);
            }
        });
    });
})


const deleteCashFlow = document.querySelectorAll(".delete-cashflow");

deleteCashFlow.forEach((deleteBtn)=>{
    const id = deleteBtn.dataset.id
    deleteBtn.onclick = ()=>{
        fetch("delete_cashflow", {
            method: "POST",

            body: JSON.stringify({
                cashflow_id:id
            })
        })
        .then(response => response.json())
        .then((answer)=>{
            if(answer.ok){

                location.reload()
            }else{
                alert(answer.error)
            }
        })
    }
})