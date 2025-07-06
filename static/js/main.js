document.addEventListener("DOMContentLoaded", function () {
    let universityData = {};

    // --- DOM Element References ---
    const unansweredContainer = document.getElementById("unanswered-questions-container");
    const answeredContainer = document.getElementById("answered-questions-container");
    const sectionSelect = document.getElementById('data-section-select');
    const dataEditor = document.getElementById('data-editor');
    const editValidationMsg = document.getElementById('edit-validation-message');
    const updateBtn = document.getElementById('update-data-btn');
    const addSectionBtn = document.getElementById('add-section-btn');
    const newSectionKeyInput = document.getElementById('new-section-key');
    const newSectionDataInput = document.getElementById('new-section-data');
    const addValidationMsg = document.getElementById('add-validation-message');
    const toast = document.getElementById('toast');

    // --- UI Helpers ---
    function showToast(message, type = 'success') {
        toast.textContent = message;
        toast.className = 'toast show ' + type;
        setTimeout(() => {
            toast.className = 'toast';
        }, 3000);
    }

    function validateJSON(textarea, messageElement) {
        if (textarea.value.trim() === '') {
            textarea.classList.remove('valid', 'invalid');
            messageElement.textContent = '';
            return false;
        }
        try {
            JSON.parse(textarea.value);
            textarea.classList.remove('invalid');
            textarea.classList.add('valid');
            messageElement.textContent = '';
            return true;
        } catch (e) {
            textarea.classList.remove('valid');
            textarea.classList.add('invalid');
            messageElement.textContent = e.message;
            return false;
        }
    }

    function checkAndSetScrollable() {
        if (unansweredContainer.children.length > 3) {
            unansweredContainer.classList.add("scrollable");
        } else {
            unansweredContainer.classList.remove("scrollable");
        }

        if (answeredContainer.children.length > 3) {
            answeredContainer.classList.add("scrollable");
        } else {
            answeredContainer.classList.remove("scrollable");
        }
    }

    // --- Question Management ---
    function createQuestionCard(item) {
        const div = document.createElement("div");
        div.className = "question-item";
        div.innerHTML = `<div class="question-text">${item.question}</div>`;
        const submitBtn = document.createElement('button');
        submitBtn.className = 'btn btn-answer';
        submitBtn.innerHTML = `<i data-feather="send"></i> Mark as Answered`;
        submitBtn.onclick = () => {
            fetch("/answer_question", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        question: item.question
                    })
                })
                .then(res => res.json())
                .then(result => {
                    if (result.success) {
                        div.remove();
                        answeredContainer.appendChild(createAnsweredCard({
                            question: item.question,
                            answer: "Marked as answered."
                        }));
                        showToast("Question marked as answered!");
                        checkAndSetScrollable();
                        feather.replace(); // Re-run Feather icons
                    } else {
                        showToast('Error: ' + result.error, 'error');
                    }
                });
        };
        div.appendChild(submitBtn);
        return div;
    }

    function createAnsweredCard(item) {
        const div = document.createElement("div");
        div.className = "answered-item";
        div.innerHTML = `<div><strong>Q:</strong> ${item.question}</div><div style="color: var(--secondary-text-color);"><strong>A:</strong> ${item.answer}</div>`;
        const undoBtn = document.createElement('button');
        undoBtn.className = 'btn btn-undo';
        undoBtn.innerHTML = `<i data-feather="undo"></i> Undo`;
        undoBtn.onclick = () => {
            fetch("/undo_answer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: item.question
                })
            })
            .then(res => res.json())
            .then(result => {
                if (result.success) {
                    div.remove();
                    unansweredContainer.appendChild(createQuestionCard({
                        question: item.question
                    }));
                    showToast("Question moved back to inbox!");
                    checkAndSetScrollable();
                    feather.replace();
                } else {
                    showToast('Error: ' + result.error, 'error');
                }
            });
        };
        div.appendChild(undoBtn);
        return div;
    }


    // --- University Data Editor ---
    function populateSectionDropdown() {
        sectionSelect.innerHTML = '<option value="">-- Select a Section --</option>';
        Object.keys(universityData).sort().forEach(key => {
            const option = document.createElement('option');
            option.value = key;
            option.innerText = key;
            sectionSelect.appendChild(option);
        });
    }

    async function fetchAllData() {
        try {
            // Fetch university data first to populate editor correctly
            const uniResponse = await fetch("/get_university_data");
            const uniData = await uniResponse.json();
            if (uniData.error) {
                showToast("Error loading university data.", "error");
                return;
            }
            universityData = uniData;
            populateSectionDropdown();

            // Fetch questions
            const questionsResponse = await fetch("/get_questions");
            const questionsData = await questionsResponse.json();
            unansweredContainer.innerHTML = "";
            questionsData.unanswered.forEach(item => unansweredContainer.appendChild(createQuestionCard(item)));

            // Fetch answered questions
            const answeredResponse = await fetch("/get_answered_questions");
            const answeredData = await answeredResponse.json();
            answeredContainer.innerHTML = "";
            answeredData.answered.forEach(item => answeredContainer.appendChild(createAnsweredCard(item)));

            checkAndSetScrollable(); // Call this function after loading the questions
        } catch (error) {
            showToast("Failed to fetch data from the server.", "error");
        }
    }

    // --- Event Listeners ---
    dataEditor.addEventListener('keyup', () => validateJSON(dataEditor, editValidationMsg));
    newSectionDataInput.addEventListener('keyup', () => validateJSON(newSectionDataInput, addValidationMsg));

    sectionSelect.addEventListener('change', (event) => {
        const selectedKey = event.target.value;
        dataEditor.value = selectedKey && universityData[selectedKey] ?
            JSON.stringify(universityData[selectedKey], null, 4) :
            '';
        validateJSON(dataEditor, editValidationMsg);
    });

    updateBtn.addEventListener('click', () => {
        if (!validateJSON(dataEditor, editValidationMsg) || dataEditor.value === '') return;
        const selectedKey = sectionSelect.value;
        if (!selectedKey) {
            showToast("Please select a section to update.", "error");
            return;
        }

        fetch('/update_section', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    section: selectedKey,
                    data: dataEditor.value
                })
            })
            .then(res => res.json())
            .then(result => {
                if (result.success) {
                    showToast(`Section '${selectedKey}' updated successfully!`);
                    fetchAllData();
                } else {
                    showToast(`Error: ${result.error}`, 'error');
                }
            });
    });

    addSectionBtn.addEventListener('click', () => {
        if (!validateJSON(newSectionDataInput, addValidationMsg) || newSectionDataInput.value === '') return;
        const newKey = newSectionKeyInput.value.trim();
        if (!newKey) {
            showToast("Please provide a name for the new section.", "error");
            return;
        }

        fetch('/add_section', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    key: newKey,
                    data: newSectionDataInput.value
                })
            })
            .then(res => res.json())
            .then(result => {
                if (result.success) {
                    showToast(`New section '${newKey}' added successfully!`);
                    newSectionKeyInput.value = '';
                    newSectionDataInput.value = '';
                    newSectionDataInput.classList.remove('valid', 'invalid');
                    fetchAllData();
                } else {
                    showToast(`Error: ${result.error}`, 'error');
                }
            });
    });

    // Initial data fetch on page load
    fetchAllData();
});