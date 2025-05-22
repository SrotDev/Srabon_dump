import { useState, useEffect } from "react";
import StepName from "../components/survey/StepName";
import StepClass from "../components/survey/StepClass";
import StepSubjects from "../components/survey/StepSubjects";
import StepLoading from "../components/survey/StepLoading";
import SurveyProgress from "../components/survey/SurveyProgress";
import { useNavigate } from "react-router-dom";
const token = localStorage.getItem("token");

const StudentJourneyPage = () => {
  const [step, setStep] = useState(0);
  const [name, setName] = useState("");
  const [studentClass, setStudentClass] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (step === 3) {
      // final step: POST data
      const timer = setTimeout(() => {
        fetch("http://192.168.0.106:8000/api/studentinfo/", {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
          body: JSON.stringify({
            name,
            class: studentClass,
            // subjects,
          }),
        })
          .then((res) => res.json())
          .then(() => navigate("/functionalities"))
          .catch((err) => {
            console.error("❌ Survey submission failed", err);
            navigate("/functionalities");
          });
      }, 2000);

      return () => clearTimeout(timer);
    }
  }, [step]);

  const goNext = () => {
    if (step < 3) setStep((prev) => prev + 1);
  };

  const goBack = () => {
    if (step > 0) setStep((prev) => prev - 1);
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return <StepName name={name} setName={setName} />;
      case 1:
        return <StepClass selectedClass={studentClass} setSelectedClass={setStudentClass} />;
      case 2:
        return <StepSubjects selectedSubjects={subjects} setSelectedSubjects={setSubjects} />;
      case 3:
        return <StepLoading name={name} />;
      default:
        return null;
    }
  };

  return (
    <div className="survey-container">
      <div className="survey-nav">
        <button onClick={goBack} className="nav-btn">←</button>
        <SurveyProgress step={step} />
        <button onClick={goNext} className="nav-btn">→</button>
      </div>
      {renderStep()}
    </div>
  );
};

export default StudentJourneyPage;
