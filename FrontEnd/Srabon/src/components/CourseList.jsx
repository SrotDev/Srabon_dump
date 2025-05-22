// CourseList.jsx
import { useEffect, useState } from "react";
import CourseCard from "./CourseCard";
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";

const CourseList = () => {
  const [courses, setCourses] = useState([]);
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const fetchCourses = async () => {
      const token = localStorage.getItem("token");
      const res = await fetch("http://192.168.0.106:8000/api/courses/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await res.json();
      const parsed = data.map((c) => ({
        name: c.name,
        title: c.parent?.title,
        subtitle: c.parent?.subtitle,
        subject: c.parent?.subject,
      }));
      setCourses(parsed);
    };
    fetchCourses();
  }, []);

  const next = () => setIndex((prev) => (prev + 1) % courses.length);
  const prev = () => setIndex((prev) => (prev - 1 + courses.length) % courses.length);

  const visibleCourses = courses.slice(index, index + 3);

  return (
    <div className="course-slider">
      <button onClick={prev} className="nav-btn">
        <FaArrowLeft size={24} color="#fff" />
      </button>

      <div className="course-cards">
        {visibleCourses.map((course, i) => (
          <CourseCard key={i} course={course} />
        ))}
      </div>

      <button onClick={next} className="nav-btn">
        <FaArrowRight size={24} color="#fff" />
      </button>
    </div>
  );
};

export default CourseList;
