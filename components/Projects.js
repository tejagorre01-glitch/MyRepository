import styles from './Projects.module.css'

const projects = [
  {
    title: 'High Availability Architecture on AWS',
    description: 'Designed and implemented a scalable and fault-tolerant backend system using cloud technologies to ensure high availability and performance.',
    technologies: ['AWS', 'EC2', 'Auto Scaling', 'RDS', 'S3', 'CloudFront', 'IAM'],
    link: 'https://drive.google.com/file/d/1AJ09n_u0dYqCmXgivVkd2UQ6_46ueZje/view?usp=drive_link'
  },
  {
    title: 'Expense Tracker Application',
    description: 'Built an expense tracking application using AI-assisted development to manage daily expenses and analyze spending efficiently.',
    technologies: ['Python', 'AI Tools', 'HTML', 'CSS', 'JavaScript', 'Flask', 'MySQL'],
    link: '#'
  }, 
  {
    title: 'Crop Yield Prediction using AI', 
    description: 'Developed a machine learning model using AI tools in colabratory environment to predict crop yield based on environmental and agricultural data, helping improve farming decisions..',
    technologies: ['Python', 'Machine Learning', 'Pandas', 'NumPy','Scikit-learn', 'matplotlib'],
    link: 'https://colab.research.google.com/drive/1KyKLJ-D5X6hfKvLay_MkIPN1tPcdjunp?usp=drive_link'
  }
]

export default function Projects() {
  return (
    <section className={styles.projects} id="projects">
      <div className={styles.container}>
        <h2 className={styles.title}>My Projects</h2>
        <div className={styles.grid}>
          {projects.map((project, index) => (
            <div key={index} className={styles.card}>
              <h3>{project.title}</h3>
              <p>{project.description}</p>
              <div className={styles.technologies}>
                {project.technologies.map((tech, i) => (
                  <span key={i} className={styles.tech}>{tech}</span>
                ))}
              </div>
              <a href={project.link} className={styles.link}>View Project</a>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}