function toggleElementVisibility (element) {
    element.hidden = !element.hidden;
}

document.addEventListener('DOMContentLoaded', function () {
    var collapseButtons = document.querySelectorAll('.comparison-control__collapse');
    var collapsableBlocks = document.querySelectorAll('.comparison-block > .comparison-content');

    for (var button of collapseButtons) {
        button.addEventListener('click', function () {
            var comparisonBlock = document.getElementById(this.dataset.toggleId);

            toggleElementVisibility(comparisonBlock);
        });
    }
    
    var showDiffButtons = document.querySelectorAll('.comparison-image-control__button');

    for (var diffButton of showDiffButtons) {
        diffButton.addEventListener('click', function () {
            var diffImage = document.getElementById(this.dataset.toggleId);

            toggleElementVisibility(diffImage);
        });
    }
});
