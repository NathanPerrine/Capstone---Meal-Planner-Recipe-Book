console.log("Hello world")

{

    // Function to dynamically add ingredient forms as needed.
    function addIngredientForm(){
        // Spot to append
        ingredientSpot = document.getElementById('ingredients')

        // Bootstrap row and columns
        const row = document.createElement('div')
        row.className = "row"
        const amtDiv = document.createElement('div')
        amtDiv.className = "col-3"
        const ingDiv = document.createElement('div')
        ingDiv.className = "col-9"

        // Ingredients
        const ingredientLabel = document.createElement('label')
        ingredientLabel.for = "ingredint"
        ingredientLabel.innerHTML = "Ingredient"
        const ingredientInput = document.createElement('input')
        ingredientInput.type = "text"
        ingredientInput.className = "form-control"
        ingredientInput.id = "ingredient"
        ingredientInput.name = "ingredient"
        ingredientInput.placeholder = "Ingredient"

        // Amounts
        const amountLabel = document.createElement('label')
        amountLabel.for = "amount"
        amountLabel.innerHTML = "Amount"
        const amountInput = document.createElement('input')
        amountInput.type = "text"
        amountInput.className = "form-control"
        amountInput.id = "amount"
        amountInput.name = "amount"
        amountInput.placeholder = "Amount"

        // Add amounts to amtDiv
        amtDiv.append(amountLabel)
        amtDiv.append(amountInput)
        // Add ingredients to ingDiv
        ingDiv.append(ingredientLabel)
        ingDiv.append(ingredientInput)
        // Add divs/cols to Row
        row.append(amtDiv)
        row.append(ingDiv)
        // add Row to ingredientSpot
        ingredientSpot.append(row)

    }


}