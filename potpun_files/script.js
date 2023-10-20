// Assuming the data is in JSON format
let words = [];
let suggestions = {};
let next_word = {};

function getCurrentWord(textarea) {
    const text = textarea.value;
    const start = textarea.selectionStart;
    let end = start;

    while (end > 0 && /\S/.test(text[end - 1])) {
        end--;
    }

    return text.substring(end, start);
}

function getPreviousWord(textarea) {
    const text = textarea.value;
    let start = textarea.selectionStart;
    let end = start;

    // Find the end of the previous word
    while (end > 0 && /\S/.test(text[end - 1])) {
        end--;
    }
    while (end > 0 && !(/\S/.test(text[end - 1]))) {
        end--;
    }

    // Find the start of the previous word
    start = end;
    while (start > 0 && /\S/.test(text[start - 1])) {
        start--;
    }

    return text.substring(start, end).trim();
}

function suggest(prefix, prevWord = null) {
    if (!prefix) {
        return [];
    }
    prevWord = prevWord ? prevWord.toLowerCase() : '';
    prefix = prefix.toLowerCase();
    let suggestionsList = [];
    const key = prevWord + prefix[0];
    if (next_word[key]) {
        for (const index of next_word[key]) {
            const word = words[index];
            if (word.startsWith(prefix)) {
                suggestionsList.push(word);
                if (suggestionsList.length === 10) { 
                    return suggestionsList;
                }
            }
        }
    }
    if (suggestions[prefix]) {
        for (const index of suggestions[prefix]) {
            const word = words[index];
            if (!suggestionsList.includes(word)) {
                suggestionsList.push(word);
                if (suggestionsList.length === 10) {
                    return suggestionsList;
                }
            }
        }
    }
    return suggestionsList;
}

const editor = document.getElementById('editor');
const popup = document.getElementById('suggestions');
const languageRadios = document.getElementsByName('language');
const autoCapitalizeCheckbox = document.getElementById('autoCapitalize');
const autoSpaceInterpunctionCheckbox = document.getElementById('autoSpaceInterpunction');
const autoSpaceCompletionCheckbox = document.getElementById('autoSpaceCompletion');

let currentLanguage = 'croatian';
let autoCapitalize = true;
let autoSpaceInterpunction = true;
let autoSpaceCompletion = true;

function loadDict() {
    console.log('Fetching dictionary for', currentLanguage);
    document.getElementById('loading').style.display = 'block';
    fetch('./potpun_files/' + currentLanguage + '.json')
        .then(response => response.json())
        .then(data => {
            words = data.words;
            suggestions = data.suggestions;
            next_word = data.next_word;
            document.getElementById('loading').style.display = 'none';
        });
};

loadDict();

// Event listeners to update the settings
Array.from(languageRadios).forEach(radio => {
    radio.addEventListener('change', function() {
        currentLanguage = this.value;
        loadDict();
    });
});

autoCapitalizeCheckbox.addEventListener('change', function() {
    autoCapitalize = this.checked;
    // Implement logic for auto capitalization if needed
});

autoSpaceInterpunctionCheckbox.addEventListener('change', function() {
    autoSpaceInterpunction = this.checked;
    // Implement logic for auto spacing after interpunction if needed
});

autoSpaceCompletionCheckbox.addEventListener('change', function() {
    autoSpaceCompletion = this.checked;
    // Implement logic for auto spacing after completion if needed
});

const mirror = document.createElement('div');
mirror.id = 'mirror';
const styles = window.getComputedStyle(editor);
for (let prop of styles) {
    mirror.style[prop] = styles[prop];
}
mirror.style['position'] = 'absolute';
mirror.style['visibility'] = 'hidden';
mirror.style['overflow'] = 'hidden';
document.body.appendChild(mirror);

let completions = [];
let capitalize = true;
let space_after_interpunction_inserted = false;
let space_after_selection_inserted = false;

editor.addEventListener('keyup', function(event) {
    const currentWord = getCurrentWord(editor);
    if (space_after_selection_inserted && currentWord == '') return;

    // Clear previous suggestions
    popup.innerHTML = '';

    if (currentWord.match(/[.!?:,;]$/)) {
        if (space_after_selection_inserted) {
            editor.value = editor.value.slice(0, -2) + currentWord + ' ';
            space_after_selection_inserted = false;
        }
        else if (autoSpaceInterpunction) {
            editor.value += ' ';
            editor.selectionStart += 1;
            editor.selectionEnd += 1;
            space_after_interpunction_inserted = true;
        }
        if (/^[.!?]$/.test(currentWord) && autoCapitalize) {
            capitalize = true;
        }
        return;
    }

    space_after_selection_inserted = false;
    space_after_interpunction_inserted = false;

    const previousWord = getPreviousWord(editor);
    const suggestions = suggest(currentWord, previousWord);

    // Populate suggestions
    completions = [];
    suggestions.forEach((word, index) => {
        const div = document.createElement('div');
        let completion = currentWord + word.slice(currentWord.length);
        completions.push(completion)
        div.textContent = `${index}: ${completion}`;
        popup.appendChild(div);
    });

    // Mirror the textarea content and insert a marker at the cursor position
    const textBeforeCursor = editor.value.substring(0, editor.selectionStart);
    const textAfterCursor = editor.value.substring(editor.selectionEnd);
    mirror.innerHTML = textBeforeCursor + '<span>|</span>' + textAfterCursor;

    // Measure the marker's position
    const marker = mirror.querySelector('span');
    const rect = marker.getBoundingClientRect();

    // Position suggestions near cursor
    popup.style.left = rect.left + 5 + 'px';
    popup.style.top = rect.top - 50 + 'px';
    popup.style.display = 'block';
});

editor.addEventListener('keydown', function(event) {
    // Check if this is a suggestion selection 0-9
    if (!space_after_selection_inserted && popup.innerHTML && event.keyCode >= 48 && event.keyCode <= 57) {
        event.preventDefault();  // Prevent the default behavior

        const index = event.keyCode - 48;
        let selectedWord = completions[index];
        if (autoSpaceCompletion) {
            selectedWord += ' ';
            space_after_selection_inserted = true;
        }

        if (selectedWord) {
            const currentWord = getCurrentWord(editor);
            const beforeWord = editor.value.substring(0, editor.selectionStart - currentWord.length);
            const afterWord = editor.value.substring(editor.selectionStart);

            editor.value = beforeWord + selectedWord + afterWord;

            // Move the cursor to the end of the inserted word
            editor.selectionStart = editor.selectionEnd = beforeWord.length + selectedWord.length;

            // Hide suggestions after selecting a word
            popup.style.display = 'none';
        }
    }
    if (capitalize && event.key.length === 1 && /[a-zA-Z]/.test(event.key)) {
        event.preventDefault();
        editor.value += event.key.toUpperCase();
        capitalize = false;
    }
});

document.getElementById('copyButton').addEventListener('click', function() {
    const textarea = document.getElementById('editor');
    textarea.select();
    document.execCommand('copy');
    textarea.blur();
});

