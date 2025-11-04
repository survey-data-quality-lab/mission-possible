
setwd("C:/Users/sharrs/Dropbox/Project Bot Catching/Results/_Combined_V2")

library(readxl)
library(dplyr)
library(jsonlite)
library(stringr)
library(writexl)

x <- read_excel("Data/tracker_raw.xlsx")



# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ------------------------    TRACKER JSON     ------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

# Function to provide names based on the question IDs
# These names are then used as <name>.page/paste/tab/mouseMoveCount/... convention 
# and each will have its own column
nameQuestion <- function(qList) {
  
  questionTag <- NA
  
  qList <- unlist(qList)
  
  if("QID42" %in% qList) {
    questionTag <- 'idpage'
    # print("First page spotted!")
  }
  
  if("QID19" %in% qList) {
    questionTag <- 'consent'
    # print("Second page spotted!")
  }
  
  if("QID45" %in% qList) {
    questionTag <- 'consent'
  }
  
  if("QID47" %in% qList) {
    questionTag <- 'idpage'
  }
  
  if("QID13" %in% qList) {
    questionTag <- 'comprehension'
  }
  
  if("QID21" %in% qList) {
    questionTag <- 'captcha'
  }
  
  if("QID14" %in% qList) {
    questionTag <- 'dictator'
  }
  
  if("QID40" %in% qList) {
    questionTag <- 'transitionPage'
  }
  
  if("QID16" %in% qList) {
    questionTag <- 'textInput'
  }
  
  if("QID9" %in% qList) {
    questionTag <- 'demographics'
  }
  
  if("QID38" %in% qList) {
    questionTag <- 'video'
  }
  
  
  if(is.na(questionTag)) {
    cat("unidentified question!\n")
    cat(qList, "\n")
  }
  
  return(questionTag)
  
  
}

# Either add the column to the data frame if it doesn't exist and provide the 
# respective row's value in that cell (which only occurs for the first row)
# or if the column is already generated then simply add the value for that
# respective row and column
appendOrCreate <- function(df, row, col, value) {
  
  # Create the column as a list if it doesn't exist
  if (!col %in% names(df)) {
    df[[col]] <- vector("list", nrow(df))
  }
  
  # If the current cell is NULL, initialize it as a list with the value
  if (is.null(df[[col]][[row]])) {
    
    df[[col]][[row]] <- list(value)
    
  } else {
    
    # Append the value to the existing list
    df[[col]][[row]] <- c(df[[col]][[row]], list(value))
    
  }
  
  return(df)
  
}


for(i in 1:nrow(x)) {
  
  cat("row", i, "\n")
  temp <- x$tracking_json[i]
  
  json <- tryCatch(fromJSON(temp), error = function(e) {
    return(NULL)
  })
  
  if(is.null(json)) {
    cat("invalid json in row ", i, "\n")
  } 
  
  
  for(index in 1:nrow(json)) {
    
    
    if(!is.null(json)) {
      
      # Record the variables from json
      page <- json[index,]$page
      duration <- json[index,]$time_on_page
      paste <- json[index,]$paste_detected
      copy <- json[index,]$copy_detected
      tab <- json[index,]$tab_hidden
      blur <- json[index,]$window_blurred
      mouseMoveCount <- json[index,]$mouse_move_count
      clickCount <- json[index,]$click_count
      
      questions <- nameQuestion(json[index,]$question_ids)
      
      # Name the columns
      varName.page <- questions
      varName.pageNumber <- paste0(varName.page, ".page")
      varName.duration <- paste0(varName.page, ".duration")
      varName.paste <- paste0(varName.page, '.paste')
      varName.copy <- paste0(varName.page, '.copy')
      varName.tab <- paste0(varName.page, '.tab')
      varName.blur <- paste0(varName.page, '.blur')
      varName.mouseMoveCount <- paste0(varName.page, '.mouseMoveCount')
      varName.clickCount <- paste0(varName.page, '.clickCount')
      
      # Add the cell value to the column
      # If the column does not exist (only the case with the first row), then
      # create the column with the names
      x <- appendOrCreate(x, i, varName.pageNumber, page)
      x <- appendOrCreate(x, i, varName.duration, duration)
      x <- appendOrCreate(x, i, varName.paste, paste)
      x <- appendOrCreate(x, i, varName.copy, copy)
      x <- appendOrCreate(x, i, varName.tab, tab)
      x <- appendOrCreate(x, i, varName.blur, blur)
      x <- appendOrCreate(x, i, varName.mouseMoveCount, mouseMoveCount)
      x <- appendOrCreate(x, i, varName.clickCount, clickCount)
      
      # just in case we have a case where json is not available
    } else { 
      
      cat("Warning!!!\n There is no JSON to fetch data from....\n\n")
      
      x[i, varName.pageNumber]   <- NA
      x[i, varName.duration]     <- NA
      x[i, varName.paste]        <- NA
      x[i, varName.copy]         <- NA
      x[i, varName.tab]          <- NA  
      x[i, varName.blur]         <- NA
      x[i, varName.mouseMoveCount] <- NA
      x[i, varName.clickCount]   <- NA
      
    }
    
    
  }
  
  # cat("end of loop \n ------ \n")
  
}


# ------- Aggregate over multiple JSONs of the same page -------

# Sum values (e.g. mouse movement, clicks, durations etc)
# We do not touch the page index at this stage (it won't make sense to sum those)

x[] <- lapply(names(x), function(colname) {
  col <- x[[colname]]
  
  if (is.list(col) && !grepl("\\.page$", colname)) {
    sapply(col, function(cell) {
      if (is.null(cell)) {
        
        NA
        
      } else {
        
        vals <- unlist(cell, recursive = TRUE, use.names = FALSE)
        
        if (all(is.na(vals))) {
          
          NA
          
        } else if (is.numeric(vals)) {
          
          sum(vals, na.rm = TRUE)
          
        } else if (is.logical(vals)) {
          
          any(vals, na.rm = TRUE)
          
        } else {
          paste(vals, collapse = "|")   # fallback for text
        }
      }
    })
  } else {
    # keep as is (non-lists or .page columns)
    col
    
  }
})

# Now for page indexes 
# we take say c("1","2") and convert it into a string like "1|2"

x[] <- lapply(names(x), function(colname) {
  col <- x[[colname]]
  
  if (is.list(col) && grepl("\\.page$", colname)) {
    sapply(col, function(cell) {
      if (is.null(cell)) {
        NA
      } else {
        paste(unlist(cell), collapse = "|")
      }
    })
  } else {
    col
  }
})





# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ------------------------    KEY LOG JSON     ------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #





col.names <- c("str", "copyPaste", "num", "mean", "median", "sd")
for (prefix in c("key_log")) {
  for (names in col.names) {
    x[[paste(prefix, names, sep = ".")]] <- NA
  }
}



# salvaging unfinished JSONs
# JSONs may end up being not finished because the machine may reach its memory limit
# We force finish it (salvage) via the below code, so that it becomes usable
salvage <- function(json_string) {
  
  # find all }
  brace_positions <- gregexpr(pattern = '}', json_string)[[1]]
  
  # if any }
  if (brace_positions[1] > 0) {
    
    # get the position of the last }
    last_brace_pos <- max(brace_positions)
    
    # get rid of anything after that last } 
    # if it is the end then we only got rid of ] and we will add it back
    # if it was some unfinished half ass json then we got rid of that problematic part and then again pyut the ]
    salvaged_part <- substr(json_string, 1, last_brace_pos)
    
    # add ] to make it a json again
    repaired_json <- paste0(salvaged_part, "]")
    
    return(repaired_json)
    
  } else {
    
    # needed this for cases where the whole thing was empty
    return("[]")
    
  }
  
}



count.empty <- 0
count.halfAssJSON <- 0
count.salvaged <- 0

for(i in 1:nrow(x)) {
  
  for(col.name in c("key_log")) {
    
    cell.val <- x[i, col.name][[1]]
    
    # check if there is no json or the json is empty
    if(is.na(cell.val) || cell.val == "" || cell.val == "[]") {
      
      print(i)
      
      cat("Row", i, "is skipped -> EMPTY keylog JSON")
      count.empty <- count.empty + 1
      
      next
      
    } 
    
    
    # Check if there are any JSONs that did not finish and if so "salvage" them
    if (startsWith(cell.val, "[") && !endsWith(cell.val, "]")) {
      
      cell.val <- salvage(cell.val)
      count.salvaged <- count.salvaged + 1
      
    }
    
    
    
    # now that we dealt with all edge cases let's convert the json into a data frame
    klog <- tryCatch({
      fromJSON(cell.val)
    }, error = function(e) {
      return(NULL)
    })
    
    # With the above code we should get a NULL for the klog if the JSON is
    # unfinished. Below code then checks for any unfinished JSONs that
    # we failed to salvage.
    if(is.null(klog)) {
      
      cat("Row", i, "is skipped -> UNFINISHED keylog JSON")
      
      count.halfAssJSON <- count.halfAssJSON + 1
      
      next
      
    }
    
    # calculate the time difference between each keystroke
    time.diff <- diff(klog$time)
    
    # get every element (every key stroke) in the keylog dataframe combine them 
    # into a single string, separate each key stroke with "|"
    str <- paste(klog$key, collapse = "|")
    
    # get the number of key strokes
    num <- nrow(klog)
    
    # get the average time between keystrokes
    mean <- mean(time.diff, na.rm = TRUE)
    
    # get the median time between keystrokes
    median <- median(time.diff, na.rm = TRUE)
    
    # get the standart deviation time between keystrokes
    sd <- sd(time.diff, na.rm = TRUE)
    
    # record the variables
    x[[paste0(col.name, ".", "str")]][i] <- str
    x[[paste0(col.name, ".", "num")]][i] <- num
    x[[paste0(col.name, ".", "mean")]][i] <- mean
    x[[paste0(col.name, ".", "median")]][i] <- median
    x[[paste0(col.name, ".", "sd")]][i] <- sd
    
    # look for INPUT_JUMP input in the keystroke data
    # if you find one set inputJump variable to 1 (0 otherwise)
    hasPasted <- !is.na(str) & grepl("INPUT_JUMP", str)
    
    if(!hasPasted) {
      x[[paste0(col.name, ".", "inputJump")]][i] <- 0
    } else {
      x[[paste0(col.name, ".", "inputJump")]][i] <- 1
    }
    
  }
  
}


# report on our salvage attempts and number of empty JSONs
cat("\nNumber of empty keylog JSONs:", count.empty)
cat("\nNumber of unfinished keylog JSONs:", count.halfAssJSON)
cat("\nNumber of salvaged (forced finished) unfinished keylog JSONs:", count.salvaged)

count.inputJump <- sum(x$key_log.inputJump, na.rm = TRUE)

# Report on the number of INPUT_JUMPs
cat("\nNumber of INPUT_JUMPs:", count.inputJump)



# Q16 is the text question's input

# -- word count ---
x$key_log.wordCount <- str_count(x$Q16, "\\S+")
x$key_log.wordCount[is.na(x$key_log.wordCount)] <- 0

#  -- character count ---
x$key_log.charCount <- nchar(x$Q16)
x$key_log.charCount[is.na(x$key_log.charCount)] <- 0



# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# Reconstruct Submitted Text from Keystrokes
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

x[["key_log.reconstructedInput"]] <- NA

reconstruct_text <- function(keylog.str) {
  
  # if NA or empty input, return ""
  if (is.na(keylog.str) || keylog.str == "") {
    return("")
  }
  
  keys <- unlist(strsplit(keylog.str, "\\|"))
  output <- character(0)
  
  skip_keys <- c(
    "Shift","CapsLock","INPUT_JUMP","Control","Alt","Tab",
    "ArrowUp","ArrowDown","ArrowLeft","ArrowRight",
    "Up","Down","Left","Right",
    "Home","End","PageUp","PageDown",
    "Insert","Delete","Escape", "Enter",
    "Meta"
  )
  
  i <- 1
  while (i <= length(keys)) {
    k <- keys[i]
    
    # Case 1: skip modifiers & special keys
    if (k %in% skip_keys) {
      # also skip common shortcuts like Control+c, Control+v, Control+a
      if (k == "Control" && i < length(keys)) {
        next_key <- keys[i + 1]
        if (next_key %in% c("c", "v", "a", "C", "V", "A")) {
          i <- i + 2  # skip both Control and following key
          next
        }
      }
      i <- i + 1
      next
    }
    
    # Case 2: handle backspace
    if (k == "Backspace") {
      if (length(output) > 0) {
        output <- output[-length(output)]
      }
      i <- i + 1
      next
    }
    
    # Case 3: normal character
    output <- c(output, k)
    i <- i + 1
  }
  
  # paste(output, collapse = "")
  out <- paste(output, collapse = "")
  sub("[[:space:]]+$", "", out)   # removes trailing whitespace only
  
  
}


for(i in 1:nrow(x)) {
  
  # print(i)
  
  keylog.str <- x$key_log.str[i]
  
  reconstructed <- reconstruct_text(keylog.str)
  
  x$key_log.reconstructedInput[i] <- reconstructed
  
}


x[["key_log.normDistReconOrg"]] <- NA


for (i in 1:nrow(x)) {
  
  original <- x$Q16[i]
  reconstructed <- x$key_log.reconstructedInput[i]
  
  # handle NA/empty safely
  if (is.na(original)) original <- ""
  if (is.na(reconstructed)) reconstructed <- ""
  
  # Levenshtein distance
  lev <- stringdist(reconstructed, original, method = "lv")

  # Normalized Levenshtein distance — also handle denominator=0
  denom <- max(nchar(original), nchar(reconstructed))
  if (denom == 0) {
    normalizedDist <- 1   # or 0, depending on your convention
  } else {
    normalizedDist <- 1 - lev / denom
  }
  
  # assign back to x
  x$key_log.normDistReconOrg[i] <- normalizedDist
  
  
}


# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# Export the cleaned tracker data
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


#write.csv(x, "Data/tracker.csv", row.names = FALSE)

write_xlsx(x, path = "Data/tracker.xlsx") 

