package app.corona_travel.dao;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BatchPreparedStatementSetter;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;

/**
 * Класс, осуществляющий запросы к БД
 *
 * @author Елена Карелина
 */
@Component
public class ConditionsDao {

    public ArrayList<JSONObject> getMarkersInfo() {
        return new ArrayList<JSONObject>();
    }

    /**
     * Объект для подключения к БД
     */
    @Autowired
    private JdbcTemplate jdbcTemplate;

    /**
     * Метод считывания условий задания из БД
     * @param taskId id нужного задания
     * @return список условий задания
     */
    public ArrayList<String> getConditions(int taskId) {
        return (ArrayList<String>) jdbcTemplate.queryForList("SELECT text_condition FROM conditions WHERE task = ?", String.class, taskId);
    }

    public ArrayList<JSONObject> getTaskInfo(int taskId) {
        return (ArrayList<JSONObject>) jdbcTemplate.query("SELECT task_id, course_id, task_description, lti_id FROM tasks WHERE task_id = ?;", new TaskJSONMapper(), taskId);
    }

    public String getTaskLibraries(int taskId) {
        ArrayList<String> tmp = (ArrayList<String>) jdbcTemplate.queryForList("SELECT library FROM task_library WHERE task = ?", String.class, taskId);
        return tmp.get(0);
    }

    public ArrayList<String> getLibXml(int libId) {
        return (ArrayList<String>) jdbcTemplate.queryForList("SELECT lib_xml FROM library WHERE lib_id = ?", String.class, libId);
    }

    /**
     * Метод добавления нового задания в базу данных
     * @param taskId id задания
     * @param taskDescription текст задания
     * @return результат исполнения запроса к БД
     */
    public int addTask(int taskId, int courseId, String taskDescription) {
        return jdbcTemplate.update("INSERT INTO tasks VALUES (?, ?, ?)", taskId, courseId, taskDescription);
    }

    /**
     * Метод для добавления условий задания
     * @param taskId идентификатор задания, условия которого надо добавить
     * @param conditions массив добавляемых условий
     * @return массив чисел-результатов добавления каждого условия
     */
    public int[] addConditions(int taskId, ArrayList<String> conditions) {
        return jdbcTemplate.batchUpdate("INSERT INTO conditions VALUES (?, ?)",
                new BatchPreparedStatementSetter() {

                    public void setValues(PreparedStatement ps, int i) throws SQLException {
                        ps.setString(1, conditions.get(i));
                        ps.setInt(2, taskId);
                    }

                    public int getBatchSize() {
                        return conditions.size();
                    }
                });
    }
}