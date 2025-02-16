document.addEventListener("DOMContentLoaded", function () {
    const tagSelector = document.getElementById("tag-selector");
    const selectedTagsContainer = document.getElementById("selected-tags");
    const selectedTagsInput = document.getElementById("selected-tags-input");

    let selectedTags = new Set(
        selectedTagsInput.value ? selectedTagsInput.value.split(",").map(id => id.trim()) : []
    );

    function updateHiddenInput() {
        selectedTagsInput.value = Array.from(selectedTags).join(",");
    }

    function addTag(tagId, tagName) {
        if (selectedTags.has(tagId)) return;
        selectedTags.add(tagId);
        updateHiddenInput();

        const tagBadge = document.createElement("span");
        tagBadge.className = "tag-badge badge bg-primary text-white me-1 d-inline-flex align-items-center";
        tagBadge.dataset.tagId = tagId;
        tagBadge.innerHTML = `
            ${tagName}
            <button type="button" class="remove-tag btn-close btn-close-white ms-2" aria-label="Close" data-tag-id="${tagId}"></button>
        `;
        selectedTagsContainer.appendChild(tagBadge);
    }

    function removeTag(tagId) {
        selectedTags.delete(tagId);
        updateHiddenInput();
        document.querySelectorAll(`[data-tag-id="${tagId}"]`).forEach(el => el.remove());
    }

    // ✅ Включаем Select2 с поиском
    $(tagSelector).select2({
        placeholder: "Choose tag...",
        allowClear: true,
        width: "100%"
    });

    // ✅ При выборе тега он сразу добавляется
    $(tagSelector).on("select2:select", function (e) {
        const selectedOption = e.params.data;
        if (selectedOption && selectedOption.id) {
            addTag(selectedOption.id, selectedOption.text);
            $(tagSelector).val(null).trigger("change"); // Сбрасываем Select2 после выбора
        }
    });

    // ✅ Удаление тегов
    selectedTagsContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-tag")) {
            removeTag(event.target.dataset.tagId);
        }
    });

    updateHiddenInput();
});
