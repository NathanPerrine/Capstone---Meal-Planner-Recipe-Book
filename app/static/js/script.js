{
    var ingCounter = 0
    
    function setCounter(){
        //Set the current counter to the number of children divs / 3 (3 child divs, 1 row 2 cols)
        // ingredientSpot = document.getElementById('ingredients')
        let ingChildren = document.getElementById('ingredients').getElementsByTagName('div').length;
        ingCounter = (ingChildren / 3)
    }

    // Function to dynamically remove ingredient forms as needed.
    function removeIngredientForm(){
        setCounter()
        if (ingCounter > 0){
            ingCounter--
            lastRow = document.getElementById(`ing row ${ingCounter}`)
            lastRow.remove()
        }
    }
    
    // Function to dynamically add ingredient forms as needed.
    function addIngredientForm(){

        // Spot to append
        ingredientSpot = document.getElementById('ingredients')
        setCounter()

        // Bootstrap row and columns
        const row = document.createElement('div')
        row.className = `row mt-1 ingredients-${ingCounter}`
        row.id = `ing row ${ingCounter}`
        const amtDiv = document.createElement('div')
        amtDiv.className = "col-4"
        const ingDiv = document.createElement('div')
        ingDiv.className = "col-8"

        // Labels
        // Only apply the labels on the first button press
        if (ingCounter === 0){
            const ingredientLabel = document.createElement('label')
            ingredientLabel.for = "ingredint"
            ingredientLabel.innerHTML = "Ingredient"

            const amountLabel = document.createElement('label')
            amountLabel.for = "amount"
            amountLabel.innerHTML = "Amt"

            // Add labels to divs
            amtDiv.append(amountLabel)
            ingDiv.append(ingredientLabel)
        }

        const ingredientInput = document.createElement('input')
        ingredientInput.type = "text"
        ingredientInput.className = "form-control"
        ingredientInput.id = `ingredients-${ingCounter}-ingredient`
        ingredientInput.name = `ingredients-${ingCounter}-ingredient`
        ingredientInput.placeholder = "Ingredient"

        // Amounts
        
        const amountInput = document.createElement('input')
        amountInput.type = "text"
        amountInput.className = "form-control"
        amountInput.id = `ingredients-${ingCounter}-amount`
        amountInput.name = `ingredients-${ingCounter}-amount`
        amountInput.placeholder = "Amt."

        //Token
        const csrf = document.getElementById('csrf_token')
        const token = document.createElement('input')
        token.id = `ingredients-${ingCounter}-csrf_token`
        token.name = `ingredients-${ingCounter}-csrf_token`
        token.type = 'hidden'
        token.value = csrf.value


        // Add inputs to Divs
        amtDiv.append(amountInput)
        ingDiv.append(ingredientInput)
        // Add divs/cols to Row
        row.append(amtDiv)
        row.append(ingDiv)
        row.append(token)
        // add Row to ingredientSpot
        ingredientSpot.append(row)
        // Increment ingCounter
        ingCounter ++
    }
}