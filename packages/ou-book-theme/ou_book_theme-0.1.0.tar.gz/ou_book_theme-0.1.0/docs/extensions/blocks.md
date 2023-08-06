# Blocks

This page documents the additional blocks provided by the OU Book Theme

## Activity

The `{activity}` marks out a piece of practical work that is undertaken by the student:

````markdown
```{activity} Activity 1

This is an activity that you can undertake in your own time.
```
````

```{activity} Activity 1

This is an activity that you can undertake in your own time.
```

### Answer

Optionally the activity can be provided with an answer that is initially hidden:

`````markdown
````{activity} Activity 2

This is an activity you should undertake on your own, but we have also provided an answer.

```{activity-answer}
This is a sample answer for the activity, which the user can show by clicking on the link.
```
````
`````

````{activity} Activity 2

This is an activity you should undertake on your own, but we have also provided an answer.

```{activity-answer}
This is a sample answer for the activity, which the user can show by clicking on the link.
```
````

## Where Next

The `{where-next}` block is used at the end of a part to indicate that the student is ready to move on to the next part and to give
an indication of what the student can expect to see there:

````markdown
```{where-next}
You are now ready to move on to the next part.
```
````

```{where-next}
You are now ready to move on to the next part.
```

## Time

The `time` block is used to indicate that something will take a given amount of time and is generally used with `{activity}`

````markdown
```{time} 20 minutes
```
````

```{time} 20 minutes
```
