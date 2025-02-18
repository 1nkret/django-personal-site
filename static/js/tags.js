document.addEventListener("DOMContentLoaded", function () {
    const tagSelector = document.getElementById("tag-selector");
    const selectedTagsContainer = document.getElementById("selected-tags");
    const selectedTagsInput = document.getElementById("selected-tags-input");
    const addTagButton = document.getElementById("add-tag");

    let selectedTags = new Set(
        selectedTagsInput.value ? selectedTagsInput.value.split(",").filter(Boolean) : []
    );

    function updateHiddenInput() {
        const tagArray = [...selectedTags].map(tag => parseInt(tag, 10)); // Преобразуем в числа
        selectedTagsInput.value = JSON.stringify(tagArray); // Записываем в JSON
    }


    function addTag(tagId, tagName) {
        if (!tagId || selectedTags.has(tagId)) return;
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

    addTagButton.addEventListener("click", function () {
        const selectedOption = tagSelector.options[tagSelector.selectedIndex];
        if (selectedOption && selectedOption.value) {
            addTag(selectedOption.value, selectedOption.text);
        }
    });

    selectedTagsContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-tag")) {
            removeTag(event.target.dataset.tagId);
        }
    });

    updateHiddenInput();
});
