document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.querySelector('select[name="type"]');
    const categorySelect = document.querySelector('select[name="category"]');
    const subcategorySelect = document.querySelector('select[name="subcategory"]');

    function updateCategories() {
        const selectedType = typeSelect.value;
        const allowedCategories = relations.type_categories[selectedType] || [];

        Array.from(categorySelect.options).forEach(option => {
            if (!option.value || allowedCategories.includes(parseInt(option.value))) {
                option.hidden = false;
            } else {
                option.hidden = true;
            }
        });

        // Сбросить выбор, если текущая категория невалидна
        if (!allowedCategories.includes(parseInt(categorySelect.value))) {
            categorySelect.value = "";
        }

        updateSubcategories(); // также обновить подкатегории
    }

    function updateSubcategories() {
        const selectedCategory = categorySelect.value;
        const allowedSubcategories = relations.category_subcategories[selectedCategory] || [];

        Array.from(subcategorySelect.options).forEach(option => {
            if (!option.value || allowedSubcategories.includes(parseInt(option.value))) {
                option.hidden = false;
            } else {
                option.hidden = true;
            }
        });

        if (!allowedSubcategories.includes(parseInt(subcategorySelect.value))) {
            subcategorySelect.value = "";
        }
    }

    typeSelect.addEventListener('change', updateCategories);
    categorySelect.addEventListener('change', updateSubcategories);

    // Запуск при загрузке страницы
    updateCategories();
});