package app

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"

	"appengine/datastore"

	"appengine"
)

// Student is a database record for a student's profile
type Student struct {
	ID        int64
	Name      string
	TotalLaps int
}

func init() {
	http.HandleFunc("/upload", importCSV)
	http.HandleFunc("/lap", trackStudent)
	http.HandleFunc("/unlap", decrementStudent)
	http.HandleFunc("/export.csv", exportCSV)
	http.Handle("/", http.FileServer(http.Dir("public")))
}

func saveStudent(ctx appengine.Context, student *Student) error {
	key := datastore.NewKey(ctx, "Student", "", student.ID, nil)
	_, err := datastore.Put(ctx, key, student)
	return err
}

func importCSV(rw http.ResponseWriter, req *http.Request) {
	ctx := appengine.NewContext(req)

	f, _, err := req.FormFile("file")
	if err != nil {
		fmt.Fprintf(rw, "Error loading file: %s", err.Error())
		return
	}

	rows := csv.NewReader(f)
	rows.FieldsPerRecord = 3

	records, err := rows.ReadAll()
	if err != nil {
		fmt.Fprintf(rw, "Error loading file: %s", err.Error())
		return
	}

	students, err := parseStudents(ctx, records)
	if err != nil {
		fmt.Fprintf(rw, "Error loading file: %s", err.Error())
		return
	}

	keys := make([]*datastore.Key, len(students))
	for i := range keys {
		keys[i] = datastore.NewKey(ctx, "Student", "", students[i].ID, nil)
	}

	_, err = datastore.PutMulti(ctx, keys, students)
	if err != nil {
		fmt.Fprintf(rw, "Error loading file: %s", err.Error())
		return
	}

	fmt.Fprintf(rw, "Saved %d students", len(students))
}

func parseStudents(ctx appengine.Context, records [][]string) ([]Student, error) {
	// The -1 is here because we are ignoring the headers
	var students = make([]Student, 0, len(records)-1)
	for _, row := range records[1:] {
		name, idString, lapString := row[0], row[1], row[2]
		id, err := strconv.ParseInt(idString, 10, 64)
		if err != nil {
			return nil, fmt.Errorf("invalid id (%s): %s", idString, err.Error())
		}

		laps, err := strconv.Atoi(lapString)
		if err != nil {
			return nil, fmt.Errorf("invalid lap field (%s): %s", lapString, err.Error())
		}

		students = append(students, Student{
			ID:        id,
			Name:      name,
			TotalLaps: laps,
		})
	}

	return students, nil
}

func exportCSV(rw http.ResponseWriter, req *http.Request) {
	rw.Header().Set("Content-Type", "text/csv")
	output := csv.NewWriter(rw)
	output.Write([]string{"Name", "ID", "Laps"})
	ctx := appengine.NewContext(req)
	query := datastore.NewQuery("Student")
	iter := query.Run(ctx)
	for {
		var student Student
		_, err := iter.Next(&student)
		if err == datastore.Done {
			break
		} else if err != nil {
			fmt.Fprintln(rw, err.Error())
			return
		}
		err = output.Write([]string{
			student.Name,
			strconv.FormatInt(student.ID, 10),
			strconv.Itoa(student.TotalLaps),
		})
		if err != nil {
			fmt.Fprintln(rw, err.Error())
		}
	}
	output.Flush()
	err := output.Error()
	if err != nil {
		fmt.Fprintln(rw, err.Error())
	}
}

func trackStudent(rw http.ResponseWriter, req *http.Request) {
	id, err := strconv.ParseInt(req.FormValue("id"), 10, 64)
	if err != nil {
		fmt.Fprintln(rw, err.Error())
		return
	}
	ctx := appengine.NewContext(req)
	var student Student
	err = datastore.RunInTransaction(ctx, func(ctx appengine.Context) error {
		key := datastore.NewKey(ctx, "Student", "", id, nil)
		err := datastore.Get(ctx, key, &student)
		if err != nil {
			return err
		}
		student.TotalLaps++
		_, err = datastore.Put(ctx, key, &student)
		if err != nil {
			return err
		}
		return nil
	}, nil)
	if err != nil {
		fmt.Fprintln(rw, err.Error())
	}

	json.NewEncoder(rw).Encode(map[string]interface{}{
		"student": student,
	})
}

func decrementStudent(rw http.ResponseWriter, req *http.Request) {
	id, err := strconv.ParseInt(req.FormValue("id"), 10, 64)
	if err != nil {
		fmt.Fprintln(rw, err.Error())
		return
	}
	ctx := appengine.NewContext(req)
	var student Student
	err = datastore.RunInTransaction(ctx, func(ctx appengine.Context) error {
		key := datastore.NewKey(ctx, "Student", "", id, nil)
		err := datastore.Get(ctx, key, &student)
		if err != nil {
			return err
		}
		student.TotalLaps--
		_, err = datastore.Put(ctx, key, &student)
		if err != nil {
			return err
		}
		return nil
	}, nil)
	if err != nil {
		fmt.Fprintln(rw, err.Error())
	}

	json.NewEncoder(rw).Encode(map[string]interface{}{
		"student": student,
	})
}
