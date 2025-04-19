document.addEventListener("DOMContentLoaded", function () {
    const typeSelect = document.getElementById("id_type");
    const categorySelect = document.getElementById("id_category");
    const subcategorySelect = document.getElementById("id_subcategory");

    function updateCategories() {
        const typeId = typeSelect.value;
        const currentCategory = categorySelect.value;

        categorySelect.innerHTML = '<option value="">---------</option>';
        CATEGORIES.filter(cat => cat.type_id == typeId).forEach(cat => {
            const selected = cat.id == currentCategory ? 'selected' : '';
            categorySelect.innerHTML += `<option value="${cat.id}" ${selected}>${cat.name}</option>`;
        });

        updateSubcategories();
    }

    function updateSubcategories() {
        const categoryId = categorySelect.value;
        const currentSubcategory = subcategorySelect.value;

        subcategorySelect.innerHTML = '<option value="">---------</option>';
        SUBCATEGORIES.filter(sub => sub.category_id == categoryId).forEach(sub => {
            const selected = sub.id == currentSubcategory ? 'selected' : '';
            subcategorySelect.innerHTML += `<option value="${sub.id}" ${selected}>${sub.name}</option>`;
        });
    }

    typeSelect.addEventListener("change", updateCategories);
    categorySelect.addEventListener("change", updateSubcategories);

    //  Инициализируем выбор сразу после загрузки
    updateCategories();
    updateSubcategories();
});
